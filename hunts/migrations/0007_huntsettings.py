# Generated by Django 4.0.1 on 2022-01-07 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hunts", "0006_start_end_times"),
    ]

    operations = [
        migrations.CreateModel(
            name="HuntSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "google_drive_folder_id",
                    models.CharField(blank=True, max_length=128),
                ),
                (
                    "google_sheets_template_file_id",
                    models.CharField(blank=True, max_length=128),
                ),
                ("google_drive_human_url", models.URLField(blank=True)),
                ("discord_guild_id", models.CharField(blank=True, max_length=128)),
                (
                    "discord_puzzle_announcements_channel_id",
                    models.CharField(blank=True, max_length=128),
                ),
                (
                    "discord_text_category",
                    models.CharField(
                        blank=True, default="text [puzzles]", max_length=128
                    ),
                ),
                (
                    "discord_voice_category",
                    models.CharField(
                        blank=True, default="voice [puzzles]", max_length=128
                    ),
                ),
                (
                    "discord_archive_category",
                    models.CharField(blank=True, default="archive", max_length=128),
                ),
                (
                    "discord_devs_role",
                    models.CharField(blank=True, default="dev", max_length=128),
                ),
                (
                    "hunt",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="settings",
                        to="hunts.hunt",
                    ),
                ),
            ],
        ),
    ]
