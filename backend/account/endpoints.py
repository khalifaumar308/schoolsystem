from .models import Profile, SchoolUser
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
# from .functions import send_mail 
from django.http import JsonResponse
from .models import SchoolUser, Attendance
from .serializers import AttendanceSerializer
from .utils import generate_username, get_otp_html_message, send_mailer
from django.utils.crypto import get_random_string 
from .forms import AddUserForm



class AddUser(APIView):
    def post(self, request):
        print("*(****************")
        form = AddUserForm(request.POST)
        if form.is_valid():
            pin = get_random_string(length=6, allowed_chars="1234567890") 
            roles = form.cleaned_data.get("roles")
            username = generate_username(roles)

            new_user = SchoolUser.create_user(
                first_name=form.cleaned_data["first_name"],
                middle_name=form.cleaned_data["middle_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                parent_id=form.cleaned_data["parent_id"],
                gender=form.cleaned_data["gender"],
                roles=roles,
                username=username,
                pin=pin
            )
            if new_user and type(new_user) is not dict:
                mail_data = dict(
                            recipient=form.cleaned_data["email"],
                            # name=form.cleaned_data["first_name"],
                            message=f"WELCOME to SMS here is your username:{username} \n pin: {pin}",
                            otp=pin,
                            username=username
                            
                )
                send_mailer(**mail_data)
                return Response({"status":True}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status":False, "message":new_user["message"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status":False, "message":form.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetTeachers(APIView):
    def get(self, request):
        teacher = Profile.get_teachers()
        return Response(data=teacher,status=status.HTTP_200_OK)


class GetParents(APIView):
    def get(self, request):
        parent = Profile.get_parents()
        return Response(data=parent,status=status.HTTP_200_OK)


class GetStudents(APIView):
    def get(self, request):
        student = Profile.get_students()
        return Response(data=student,status=status.HTTP_200_OK)


# DASHBOARD

class GetTeacherStats(APIView):
    def get(self, request):
        stats = Profile.get_teacher_stat()
        return Response(data=stats, status=status.HTTP_200_OK)


class Attendance(APIView):
    serializer_class = AttendanceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.save_attendance(request.data)
        return Response({"success":True}, status=status.HTTP_201_CREATED)