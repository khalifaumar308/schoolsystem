from django.urls import path 
from .views import (AddTeacherAPIView,
         TeacherAccountUpdateAPIView,
         TeacherRetrieveAPIView, 
         TeacherDeleteAPIView,
         GetTeachers
         
         )
from .dashboard_endpoint import (
    GetTeacherStats
)
from .endpoints import *

urlpatterns = [
    # users
    path('user/', AddUser.as_view()),

    # teacher endpoints
    path('add_teacher/', AddTeacherAPIView.as_view()),
    path('list_teachers/', GetTeachers.as_view(), name='list-teachers'),
    path('teacher/update/<str:username>/', TeacherAccountUpdateAPIView.as_view(), name='update-teacher-account'),
     path('teacher/view/', TeacherRetrieveAPIView.as_view(), name='teacher-detail'),
     path('teacher/delete/<str:username>/', TeacherDeleteAPIView.as_view(), name='teacher-delete'),
    
    #  dashboard endpoints
     path('total_teacher', GetTeacherStats.as_view(), name='total_teacher'),
]