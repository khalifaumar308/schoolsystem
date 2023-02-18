from django.urls import path 
from .endpoints import *

urlpatterns = [
    path('attendance/', Attendance_api.as_view()),
    path("register_user", AddUser.as_view()),
    path("add_class", AddClass.as_view()),
    path("list_teachers", GetTeachers.as_view()),
    path("list_students", GetStudents.as_view()),
    path("list_parents", GetParents.as_view()),
    path("list_classes", GetClass.as_view()),
    path("total_teacher", GetTeacherStats.as_view()),
]

