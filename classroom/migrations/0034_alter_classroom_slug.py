# Generated by Django 4.0.4 on 2022-05-20 06:01

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("classroom", "0033_alter_college_allowed_dba_list"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classroom",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True,
                editable=False,
                populate_from=[
                    "title",
                    "level",
                    "stream",
                    "section",
                    "start_year",
                    "end_year",
                    "college__name",
                ],
            ),
        ),
    ]
