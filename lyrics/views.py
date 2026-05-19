from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json

from core.models import Profile
from .models import Song, LyricsProgress
from quests.progress import check_quest_progress
from daily.progress import complete_daily_activity


def _song_to_dict(song, progress=None):
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "lyrics": song.lyrics,
        "created_at": song.created_at.isoformat(),
        "lines_unlocked": progress.lines_unlocked if progress else 2,
        "last_studied": progress.last_studied.isoformat() if progress and progress.last_studied else None,
    }


@login_required
@require_http_methods(["GET"])
def songs_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    songs = Song.objects.filter(profile=profile)
    progress_map = {
        p.song_id: p
        for p in LyricsProgress.objects.filter(profile=profile, song__in=songs)
    }
    data = [_song_to_dict(song, progress_map.get(song.id)) for song in songs]
    return JsonResponse(data, safe=False)


@login_required
@require_http_methods(["POST"])
def song_create(request):
    profile = get_object_or_404(Profile, user=request.user)
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    title = body.get("title", "").strip()
    lyrics = body.get("lyrics", "").strip()
    if not title or not lyrics:
        return JsonResponse({"error": "title and lyrics are required"}, status=400)

    song = Song.objects.create(
        profile=profile,
        title=title,
        artist=body.get("artist", "").strip(),
        lyrics=lyrics,
    )
    LyricsProgress.objects.create(profile=profile, song=song)
    return JsonResponse(_song_to_dict(song), status=201)


@login_required
@require_http_methods(["GET"])
def song_detail(request, song_id):
    profile = get_object_or_404(Profile, user=request.user)
    song = get_object_or_404(Song, id=song_id, profile=profile)
    progress, _ = LyricsProgress.objects.get_or_create(profile=profile, song=song)
    return JsonResponse(_song_to_dict(song, progress))


@login_required
@require_http_methods(["POST"])
def song_update(request, song_id):
    profile = get_object_or_404(Profile, user=request.user)
    song = get_object_or_404(Song, id=song_id, profile=profile)
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if "title" in body:
        song.title = body["title"].strip()
    if "artist" in body:
        song.artist = body["artist"].strip()
    if "lyrics" in body:
        song.lyrics = body["lyrics"].strip()
    song.save()

    progress, _ = LyricsProgress.objects.get_or_create(profile=profile, song=song)
    return JsonResponse(_song_to_dict(song, progress))


@login_required
@require_http_methods(["POST"])
def song_delete(request, song_id):
    profile = get_object_or_404(Profile, user=request.user)
    song = get_object_or_404(Song, id=song_id, profile=profile)
    song.delete()
    return JsonResponse({"status": "ok"})


@login_required
@require_http_methods(["POST"])
def reset_progress(request, song_id):
    profile = get_object_or_404(Profile, user=request.user)
    song = get_object_or_404(Song, id=song_id, profile=profile)
    progress, _ = LyricsProgress.objects.get_or_create(profile=profile, song=song)
    progress.lines_unlocked = 0
    progress.last_studied = None
    progress.save()
    return JsonResponse(_song_to_dict(song, progress))


@login_required
@require_http_methods(["POST"])
def complete_session(request, song_id):
    """
    Called after a practice session. Unlocks the next 2 lines if the user
    successfully completed the current set. Grants XP + keys on each progression.
    """
    profile = get_object_or_404(Profile, user=request.user)
    song = get_object_or_404(Song, id=song_id, profile=profile)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    success = body.get("success", False)
    progress, _ = LyricsProgress.objects.get_or_create(profile=profile, song=song)
    progress.last_studied = timezone.now().date()

    total_lines = len([l for l in song.lyrics.splitlines() if l.strip()])
    already_finished = progress.lines_unlocked >= total_lines
    newly_finished = False

    if success and not already_finished:
        progress.lines_unlocked = min(progress.lines_unlocked + 2, total_lines)
        newly_finished = progress.lines_unlocked >= total_lines
        profile.experience += 10
        profile.add_keys(3)
        profile.save()
        check_quest_progress(profile, 'learn_lyrics')
        complete_daily_activity(profile, 'lyrics_game', str(song_id))

    progress.save()

    return JsonResponse({
        "status": "ok",
        "lines_unlocked": progress.lines_unlocked,
        "total_lines": total_lines,
        "finished": progress.lines_unlocked >= total_lines,
        "newly_finished": newly_finished,
        "updated_xp": profile.experience,
        "level": profile.get_level(),
        "progress": round(profile.get_progression_ratio(), 2),
    })
