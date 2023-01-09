from django.urls import path 
from .views import (AddTeacherAPIView,
         TeacherAccountUpdateAPIView,
         TeacherRetrieveAPIView, 
         TeacherDeleteAPIView
         )


urlpatterns = [
    path('add-teacher/', AddTeacherAPIView.as_view()),
    path('teacher/update/<str:username>/', TeacherAccountUpdateAPIView.as_view(), name='update-teacher-account'),
     path('teacher/view/', TeacherRetrieveAPIView.as_view(), name='teacher-detail'),
     path('teacher/delete/<str:username>/', TeacherDeleteAPIView.as_view(), name='teacher-delete')
]