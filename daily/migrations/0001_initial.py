from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_goal', models.PositiveIntegerField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_programs', to='core.profile')),
            ],
            options={
                'unique_together': {('profile', 'date')},
            },
        ),
        migrations.CreateModel(
            name='DailyActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(choices=[('lesson', 'Cours'), ('notes_reading', 'Lecture de notes'), ('blind_test', 'Blind test'), ('scales_builder', 'Construction de gammes')], max_length=30)),
                ('activity_ref', models.CharField(blank=True, max_length=100)),
                ('activity_title', models.CharField(max_length=150)),
                ('estimated_minutes', models.PositiveIntegerField(default=3)),
                ('order', models.PositiveIntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='daily.dailyprogram')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
