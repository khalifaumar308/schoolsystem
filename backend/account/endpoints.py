from .models import SchoolUser
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
# from .functions import send_mail 
from django.http import JsonResponse


class AddUser(APIView):
    def post(self, request):
        first_name = request.data.get("first_name", None)
        last_name = request.data.get("last_name", None)
        middle_name = request.data.get("middle_name", None)
        parent_id = request.data.get("parent_id", None)
        roles = request.data.get("roles", None)
        user_dict = dict(first_name=first_name, last_name=last_name, parent_id=parent_id, roles=roles, middle_name=middle_name)
        new_user = SchoolUser.create_user(**user_dict)
        if new_user:
            return Response({"success":True}, status=status.HTTP_201_CREATED)
        return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)
