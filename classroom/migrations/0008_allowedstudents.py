# Generated by Django 4.0.4 on 2022-05-09 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("classroom", "0007_student"),
    ]

    operations = [
        migrations.CreateModel(
            name="AllowedStudents",
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
                ("email", models.EmailField(max_length=255, verbose_name="Email Id")),
                (
                    "university_roll",
                    models.PositiveBigIntegerField(
                        help_text="Your University Roll No - (e.g. - 13071020030)",
                        verbose_name="University Roll",
                    ),
                ),
                (
                    "classroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="allowed_students",
                        to="classroom.classroom",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Allowed Students",
                "ordering": ["university_roll"],
                "unique_together": {
                    ("university_roll", "email"),
                    ("university_roll", "classroom"),
                    ("classroom", "email"),
                },
            },
        ),
    ]
