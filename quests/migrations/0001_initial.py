from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=255)),
                ('quest_type', models.CharField(choices=[('read_lesson', 'Lire des cours'), ('play_notes_reading', 'Jouer à Lecture de notes')], max_length=40)),
                ('required_count', models.PositiveIntegerField(default=1)),
                ('xp_reward', models.PositiveIntegerField(default=10)),
                ('keys_reward', models.PositiveIntegerField(default=2)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='UserQuest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.PositiveIntegerField(default=0)),
                ('claimed', models.BooleanField(default=False)),
                ('claimed_at', models.DateTimeField(blank=True, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_quests', to='core.profile')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_quests', to='quests.quest')),
            ],
            options={
                'unique_together': {('profile', 'quest')},
            },
        ),
    ]
