from django.db import models

from users.models import User


class Faculty(models.Model):
    name = models.TextField()


class Course(models.Model):
    name = models.CharField(max_length=100)
    credits = models.SmallIntegerField(null=True, blank=True)
    code = models.CharField(max_length=20, null=True, blank=True)
    control_type = models.CharField(
        choices=(
            ('EXAM', 'Экзамен'),
            ('PROJECT', 'Проект'),
            ('REPORT', 'Отчёт'),
        ),
        null=True, blank=True, max_length=10
    )
    lecture_hours = models.SmallIntegerField(null=True, blank=True)
    practice_hours = models.SmallIntegerField(null=True, blank=True)
    sis_hours = models.SmallIntegerField(null=True, blank=True)
    tsis_hours = models.SmallIntegerField(null=True, blank=True)

    faculty = models.ForeignKey(
        to=Faculty,
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )


class Evaluation(models.Model):
    name = models.TextField()
    photo = models.ImageField()


class Rubric(models.Model):
    name = models.TextField()


class Topic(models.Model):
    name = models.TextField()
    materials = models.TextField()
    week = models.SmallIntegerField()


class Syllabus(models.Model):
    created_by = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.DO_NOTHING)

    status = models.CharField(
        choices=(
            ('IN_PROGRESS', 'В работе'),
            ('ON_APPROVING', 'На согласовании'),
            ('ON_REGISTRATION', 'На регистрации'),
            ('ACTIVE', 'Действителен'),
            ('ON_REWORK', 'На доработке')
        ),
        max_length=40
    )
    course = models.ForeignKey(to=Course, on_delete=models.DO_NOTHING,)
    language = models.CharField(
        choices=(
            ('KZ', 'Казахский'),
            ('RU', 'Русский'),
            ('EN', 'Английский')
        ), max_length=40
    )
    year = models.CharField(max_length=20, null=True, blank=True)

    teachers = models.ManyToManyField(to=User, related_name='syllabuses')
    purpose = models.TextField(null=True, blank=True)
    tasks = models.TextField(null=True, blank=True)
    results = models.TextField(null=True, blank=True)
    methods = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    resources = models.TextField(null=True, blank=True)
    policy = models.TextField(null=True, blank=True)

    pre_courses = models.ManyToManyField(to=Course, related_name='syllabuses_pre', default=[], blank=True)
    post_courses = models.ManyToManyField(to=Course, related_name='syllabuses_post', default=[], blank=True)

    evaluation = models.ForeignKey(to=Evaluation, on_delete=models.DO_NOTHING, null=True, blank=True)
    rubric = models.ForeignKey(to=Rubric, on_delete=models.DO_NOTHING, null=True, blank=True)
    topics = models.ManyToManyField(to=Topic, null=True, blank=True)


class Approver(models.Model):
    syllabus = models.ForeignKey(to=Syllabus, related_name='approvers', on_delete=models.CASCADE)
    type = models.CharField(choices=(('COORDINATOR', 'Координатор'), ('DEAN', 'Декан')), max_length=20)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)


