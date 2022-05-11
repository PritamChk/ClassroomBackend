# Generated by Django 4.0.4 on 2022-05-11 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classroom", "0015_alter_teacher_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classroom",
            name="teachers",
            field=models.ManyToManyField(
                blank=True, related_name="classrooms", to="classroom.teacher"
            ),
        ),
    ]
