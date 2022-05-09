# Generated by Django 4.0.4 on 2022-05-09 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0009_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.TextField(default='No Heading Given', verbose_name='Heading')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Description[Optional] ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At ')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='classroom.teacher')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='classroom.subject')),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
            },
        ),
    ]
