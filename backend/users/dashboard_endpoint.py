from .models import TeacherAccount
from .serializers import OtherUserSerializer, TeacherAccountSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



# class GetTotalTeacher(APIView):
#     def get(self, request):
#         date = request.data.get("date", None)
#         print(date)
#         total = TeacherAccount.total_teachers(date)
#         print("____________+++++++++_______")
#         print(total)
#         # TODO : use date to get all teachers
#         return JsonResponse(data=total, safe=False)

class GetTeacherStats(APIView):
    def get(self, request):
        stats = TeacherAccount.get_teacher_stat()
        return Response(data=stats, status=status.HTTP_200_OK)

class GetTeacherPercentage(APIView):
    def get(self, request):
        stats = TeacherAccount.percentage_new_teachers_per_month()
        return Response(data=stats, status=status.HTTP_200_OK)