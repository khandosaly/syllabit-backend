from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from syllabus.models import Syllabus, Course, Evaluation, Topic, Approver
from users.models import User


class TopicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('name', 'week')


class SyllabusCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syllabus
        fields = ('status', 'course', 'language', 'year', 'teachers',
                  'purpose', 'tasks', 'results', 'methods', 'description',
                  'resources', 'policy', 'pre_courses', 'post_courses',
                  'evaluation', 'created_by')


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('__all__')


class TeacherSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'degree', 'job_title', 'email')


class EvaluationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ('__all__')


class ApproverCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approver
        fields = ('__all__')


class ApproverGetSerializer(serializers.ModelSerializer):
    user = TeacherSearchSerializer()
    type = SerializerMethodField()

    class Meta:
        model = Approver
        fields = ('__all__')

    def get_type(self, obj):
        if obj.type == 'COORDINATOR':
            return 'Координатор'
        if obj.type == 'DEAN':
            return 'Декан'


class SyllabusRetrieveSerializer(serializers.ModelSerializer):
    status = SerializerMethodField()
    course = CourseListSerializer()
    evaluation = EvaluationCreateSerializer()
    topics = TopicCreateSerializer(many=True)
    pre_courses = CourseListSerializer(many=True)
    post_courses = CourseListSerializer(many=True)
    teachers = TeacherSearchSerializer(many=True)
    approvers = ApproverGetSerializer(many=True)

    class Meta:
        model = Syllabus
        fields = ('__all__')

    def get_status(self, obj):
        choices = {
            'IN_PROGRESS': 'В работе',
            'ON_APPROVING': 'На согласовании',
            'ON_REGISTRATION': 'На регистрации',
            'ACTIVE': 'Действителен',
            'ON_REWORK': 'На доработке'
        }
        return choices[obj.status]

