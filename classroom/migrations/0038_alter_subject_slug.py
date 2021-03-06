# Generated by Django 4.0.4 on 2022-05-22 09:59

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("classroom", "0037_alter_stream_options_alter_subject_credit_points"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True,
                editable=False,
                populate_from=[
                    "title",
                    "semester__sem_no",
                    "subject_type",
                    "credit_points",
                    "created_by__user__first_name",
                ],
            ),
        ),
    ]
