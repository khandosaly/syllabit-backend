from django.urls import path

from syllabus.views import *

urlpatterns = [
    path("create/", SyllabusCreateView.as_view()),
    path("retrieve/<int:pk>", SyllabusRetrieveView.as_view()),
    path("recent", SyllabusRecentView.as_view()),
    path("courses", SyllabusCoursesListView.as_view()),
    path("teachers", SyllabusTeacherSearchView.as_view()),
    path("evaluation/", EvaluationListCreateView.as_view()),
    path("generate/docx/<int:pk>/", SyllabusDocxGenerateView.as_view()),
    path("sign/<int:pk>/", SyllabusSignView.as_view()),
]
