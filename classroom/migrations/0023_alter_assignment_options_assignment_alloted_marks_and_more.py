# Generated by Django 4.0.4 on 2022-05-13 16:55

import classroom.validators
import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0022_alter_assignment_options_alter_assignment_due_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['due_date', 'due_time', 'alloted_marks', '-created_at']},
        ),
        migrations.AddField(
            model_name='assignment',
            name='alloted_marks',
            field=models.PositiveSmallIntegerField(default=100, validators=[django.core.validators.MaxValueValidator(100, 'so sir you want to take exam more than 100 marks?😑')], verbose_name='Marks:'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='attached_pdf',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to='P:\\Codes\\SEM_4_Major_Project\\Code\\ClassroomBackend\\media/classroom/assignments/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'], message='Please Upload PDF file only'), classroom.validators.pdf_file_size_lt_5mb], verbose_name='Upload File Here📁'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='due_time',
            field=models.TimeField(default=datetime.datetime(2022, 5, 13, 22, 25, 15, 927058), verbose_name='Due time'),
        ),
    ]
