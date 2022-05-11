# Generated by Django 4.0.4 on 2022-05-10 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classroom", "0013_alter_college_allowed_teacher_list"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teacher",
            name="classroom",
        ),
        migrations.AddField(
            model_name="classroom",
            name="teachers",
            field=models.ManyToManyField(
                related_name="classrooms", to="classroom.teacher"
            ),
        ),
    ]
