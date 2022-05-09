# Generated by Django 4.0.4 on 2022-05-09 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syllabus', '0010_alter_syllabus_post_courses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syllabus',
            name='post_courses',
            field=models.ManyToManyField(blank=True, default=[], related_name='syllabuses_post', to='syllabus.course'),
        ),
        migrations.AlterField(
            model_name='syllabus',
            name='pre_courses',
            field=models.ManyToManyField(blank=True, default=[], related_name='syllabuses_pre', to='syllabus.course'),
        ),
    ]