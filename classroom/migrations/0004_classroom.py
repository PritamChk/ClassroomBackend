# Generated by Django 4.0.4 on 2022-05-09 20:14

import classroom.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['title', 'level', 'stream', 'section', 'start_year', 'end_year', 'college'])),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Classroom Name')),
                ('level', models.CharField(choices=[('Bachelors', 'Undergraduate'), ('Masters', 'Postgraduate')], default='Bachelors', help_text='e.g - Masters/Bachelors', max_length=40, verbose_name='Level')),
                ('stream', models.CharField(max_length=255, verbose_name='Your Stream')),
                ('start_year', models.PositiveSmallIntegerField(db_index=True, default=2020, help_text='Write your session starting year (e.g. - 2020)', validators=[django.core.validators.MinValueValidator(2000, "You can't select year less than 2000"), django.core.validators.MaxValueValidator(2023, 'Max Year Can be selected only 1 year ahead of current year')], verbose_name='Starting Year')),
                ('end_year', models.PositiveSmallIntegerField(db_index=True, default=2022, help_text='Write your session ending year (e.g. - 2020)', validators=[django.core.validators.MinValueValidator(2000, "You can't select year less than 2000"), django.core.validators.MaxValueValidator(2200, 'Max Year Can be selected only 1 year ahead of current year')], verbose_name='Ending Year')),
                ('section', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')], default='A', max_length=10, null=True, verbose_name='Section(optional)')),
                ('no_of_semesters', models.PositiveSmallIntegerField(default=4, validators=[django.core.validators.MinValueValidator(4, 'Min Course Duration is of 2 Years(4 semesters)'), django.core.validators.MaxValueValidator(14), classroom.validators.is_no_of_sem_even], verbose_name='Number of Sem')),
                ('current_sem', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(14)], verbose_name='On Going Sem')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('allowed_student_list', models.FileField(blank=True, null=True, upload_to='P:\\Codes\\SEM_4_Major_Project\\Code\\ClassroomBackend\\media/classroom/students/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv', 'xlsx'], message='Please Upload CSV/XLSX file only')], verbose_name='Upload Student List File(.csv/xl)')),
                ('allowed_teacher_list', models.FileField(blank=True, null=True, upload_to='P:\\Codes\\SEM_4_Major_Project\\Code\\ClassroomBackend\\media/classroom/teachers/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv', 'xlsx'], message='Please Upload CSV/XLSX file only')], verbose_name='Upload Teacher List File(.csv/xl)')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='classroom.college')),
            ],
            options={
                'ordering': ['college__name', 'level', '-start_year', '-end_year', 'section', 'stream'],
                'unique_together': {('level', 'stream', 'start_year', 'end_year', 'section', 'college')},
            },
        ),
    ]
