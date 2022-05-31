import base64
import json
from wsgiref.util import FileWrapper

from django.db.transaction import atomic
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, \
    UpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from syllabit import settings
from syllabus.serializers import *
from syllabus.models import Course, Evaluation, Syllabus
from syllabus.utils import save_docx, get_sign_info, sign_file
from users.models import User


class SyllabusCreateView(CreateAPIView):
    serializer_class = SyllabusCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        with atomic():
            request.data['created_by'] = self.request.user.id
            ser = SyllabusCreateSerializer(data=request.data)
            ser.is_valid(raise_exception=True)
            syl = ser.save()
            for topic in request.data.get('topics'):
                topic_ser = TopicCreateSerializer(data=topic)
                topic_ser.is_valid()
                topic_instance = topic_ser.save()
                syl.topics.add(topic_instance)
            for approver in request.data.get('approvers'):
                approver['syllabus'] = syl.id
                approver_ser = ApproverCreateSerializer(data=approver)
                approver_ser.is_valid()
                approver_instance = approver_ser.save()
                syl.approvers.add(approver_instance)
            syl.save()
            return Response(SyllabusRetrieveSerializer(syl).data)


class SyllabusRecentView(ListAPIView):
    queryset = Syllabus.objects.filter()
    serializer_class = SyllabusRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset().filter(created_by=self.request.user)
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs


class SyllabusRetrieveView(RetrieveAPIView):
    queryset = Syllabus.objects.filter()
    serializer_class = SyllabusRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class SyllabusCoursesListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = (IsAuthenticated,)


class SyllabusTeacherSearchView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = TeacherSearchSerializer
    permission_classes = (IsAuthenticated,)


class EvaluationListCreateView(ListCreateAPIView):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationCreateSerializer
    permission_classes = (IsAuthenticated,)


class SyllabusDocxGenerateView(RetrieveAPIView):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        save_docx(self.get_object())
        response = HttpResponse(
            FileWrapper(open(f'{settings.MEDIA_ROOT}syllabus_{self.get_object().id}.docx', 'rb')),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename="syllabus_{self.get_object().id}.docx"'
        return response


class SyllabusSignView(UpdateAPIView):
    queryset = Syllabus.objects.filter()
    serializer_class = SyllabusRetrieveSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        syl = self.get_object()
        approver = syl.approvers.filter(user=request.user).first()
        if not approver:
            raise APIException('Вы не подписант', 403)
        save_docx(self.get_object())

        with open(f'{settings.MEDIA_ROOT}syllabus_{self.get_object().id}.docx', 'rb') as f:
            base64_str = base64.b64encode(f.read()).decode('utf-8')

        sign_hash = sign_file(
            keystore=request.data['keystore'],
            password=request.data['password'],
            files=[{
                "fileProcessIdentifier": syl.id,
                'name': f'syllabus_{self.get_object().id}.docx',
                'content': base64_str,
                'mime': 'application/msword',
                "lifetime": "2592000000"
            }]
        )

        signer_name = json.loads(get_sign_info(
            keystore=request.data['keystore'],
            password=request.data['password']
        ).text)['subject']

        with open(f'{settings.MEDIA_ROOT}{signer_name}_{self.get_object().id}.sign', 'w+') as f:
            f.write(sign_hash)

        approver.sign_info = signer_name
        approver.signed = True
        approver.save()

        syl.status = 'ACTIVE'
        syl.save()

        response = HttpResponse(
            FileWrapper(open(f'{settings.MEDIA_ROOT}{signer_name}_{self.get_object().id}.sign', 'rb')),
            content_type='application/text'
        )
        response['Content-Disposition'] = f'attachment; filename="{signer_name}_{self.get_object().id}.sign"'
        return response


