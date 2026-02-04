from django.contrib import admin
from .models import Profile, Card, ProfileCard, CollectionCategory, CardRarity, Lesson, Instrument, InstrumentCategory, ScrollingGameLevel, MusicNote, NoteName


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nb_keys', 'experience', 'streak_count', 'last_streak_date', 'current_scrolling_game_level')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rarity')
    list_filter = ('category', 'rarity')
    search_fields = ('name',)
    ordering = ('category', 'rarity')
    fieldsets = (
        (None, {
            'fields': ('name', 'image_name', 'category', 'rarity', 'description', 'price_to_unlock')
        }),
    )


@admin.register(ProfileCard)
class ProfileCardAdmin(admin.ModelAdmin):
    list_display = ('profile', 'card', 'unlocked_at')
    list_filter = ('unlocked_at', 'card__category', 'card__rarity')
    search_fields = ('user__username', 'card__name')
    ordering = ('-unlocked_at',)


@admin.register(CollectionCategory)
class CollectionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    

@admin.register(CardRarity)
class CardRarityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Lesson)
class Lesson(admin.ModelAdmin):
    list_display = ('title', 'slug', 'chapter', 'order')


@admin.register(Instrument)
class Instrument(admin.ModelAdmin):
    list_display = ('name', 'category', 'image_name', 'level')
    

@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ScrollingGameLevel)
class ScrollingGameLevelAdmin(admin.ModelAdmin):
    list_display = ('level_number',)


@admin.register(MusicNote)
class MusicNoteAdmin(admin.ModelAdmin):
    list_display = ('note', 'position')


@admin.register(NoteName)
class NoteNameAdmin(admin.ModelAdmin):
    list_display = ('name',)