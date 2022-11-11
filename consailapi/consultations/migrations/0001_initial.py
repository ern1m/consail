# Generated by Django 4.1.2 on 2022-11-11 14:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("teachers", "0002_alter_teacher_managers"),
    ]

    operations = [
        migrations.CreateModel(
            name="Consultation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("start_time", models.DateTimeField(verbose_name="start time")),
                ("end_time", models.DateTimeField(verbose_name="end time")),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="consultations",
                        to="teachers.teacher",
                        verbose_name="teacher",
                    ),
                ),
            ],
            options={
                "verbose_name": "Consultation",
                "verbose_name_plural": "Consultations",
            },
        ),
    ]
