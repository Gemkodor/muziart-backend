# Generated by Django 5.2.3 on 2025-07-25 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_user_profilecard_profile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='price_to_unlock',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='card',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.collectioncategory'),
        ),
    ]
