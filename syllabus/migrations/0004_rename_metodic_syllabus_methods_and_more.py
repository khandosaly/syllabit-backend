# Generated by Django 4.0.4 on 2022-05-08 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syllabus', '0003_syllabus_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='syllabus',
            old_name='metodic',
            new_name='methods',
        ),
        migrations.RenameField(
            model_name='syllabus',
            old_name='post_codes',
            new_name='post_courses',
        ),
        migrations.RenameField(
            model_name='syllabus',
            old_name='pre_codes',
            new_name='pre_courses',
        ),
        migrations.RenameField(
            model_name='syllabus',
            old_name='result',
            new_name='results',
        ),
        migrations.RenameField(
            model_name='syllabus',
            old_name='teacher',
            new_name='teachers',
        ),
        migrations.RemoveField(
            model_name='syllabus',
            name='notation',
        ),
        migrations.RemoveField(
            model_name='syllabus',
            name='readings',
        ),
        migrations.RemoveField(
            model_name='syllabus',
            name='skills',
        ),
    ]