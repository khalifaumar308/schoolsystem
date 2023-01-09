from .models import TeacherAccount
from .serializers import OtherUserSerializer, TeacherAccountSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .functions import send_mail 


# class AddTeacherAPIView(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     # def get(self, request, format=None):
#     #     snippets = Snippet.objects.all()
#     #     serializer = SnippetSerializer(snippets, many=True)
#     #     return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = OtherUserSerializer(data=request.data)
#         print("==========SERIALIZER====")
#         print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddTeacherAPIView(APIView):
    serializer_class = OtherUserSerializer

    def post(self, request):
        # validate the request data using the Teacher serializer
        print('the================REQUEST')
        print(request.data, request.data.get('email', None))

        serializer = self.serializer_class(data=request.data)
        print('====SERIALIZER======')
        print(serializer, 'pop')
        serializer.is_valid(raise_exception=True)
        # first_name = serializer.data.get("first_name", None)
        # last_name = serializer.data.get("last_name", None)
        # middle_name = serializer.data.get("middle_name", None)
        # email = serializer.data.get("email", None)
        # mail_data = dict(
        #     name = f'{first_name} {middle_name} {last_name}',
        #     recipient_form = email,
        #     subject="SCHOOL REG",
        #     message=""
        # )

        # create new teacher object using the validated data
        teacher = serializer.create(validated_data=serializer.validated_data)
        if teacher:
            return Response({"success":True}, status=status.HTTP_201_CREATED)
        return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)


# class TeacherAccountUpdateAPIView(APIView):
#     def get_object(self, username):
#         try:
#             return TeacherAccount.objects.get(username=username)
#         except TeacherAccount.DoesNotExist:
#             raise Http404

#     def put(self, request, username, format=None):
#         teacher = self.get_object(username)
#         serializer = TeacherAccountSerializer(teacher, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TeacherAccountUpdateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Get the username from the query parameter
#         username = self.request.query_params.get('username')

#         # Get the TeacherAccount object with the given username
#         teacher_account = get_object_or_404(TeacherAccount, username=username)
#         print("🚀 ~ file: views.py:68 ~ teacher_account", teacher_account)

#         # Create a serializer instance with the teacher_account instance and the request data
#         serializer = TeacherAccountSerializer(teacher_account, data=request.data)

#         # Validate the data and update the teacher_account object
#         if serializer.is_valid():
#             serializer.save()
#             # Return the updated data in the response
#             return Response(serializer.data)
#         # If the data is not valid, return the errors in the response
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TeacherAccountUpdateAPIView(APIView):
#     def get_object(self, pk):
#         try:
#             return TeacherAccount.objects.get(pk=pk)
#         except TeacherAccount.DoesNotExist:
#             raise Http404
#     def post(self, request):
#         username = request.query_params.get('username')
#         teacher_account = TeacherAccount.update_teacher(username=username)
#         print('||||||||||||||||||||')
#         print(teacher_account)
#         serializer = TeacherAccountSerializer(teacher_account, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'success': 'Teacher account updated successfully'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherAccountUpdateAPIView(APIView):
    def get_object(self, username):
        try:
            return TeacherAccount.objects.get(username=username)
        except TeacherAccount.DoesNotExist:
            raise Http404

    def post(self, request, username, format=None):
        teacher_account = self.get_object(username)
        serializer = TeacherAccountSerializer(teacher_account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TeacherRetrieveAPIView(APIView):
#     def get(self, request, pk):
#         teacher = get_object_or_404(TeacherAccount, pk=pk)
#         serializer = TeacherAccountSerializer(teacher)
#         return Response(serializer.data)

class TeacherRetrieveAPIView(APIView):
    def get(self, request):
        # Get the username from the request
        username = request.query_params.get('username')
        data = TeacherAccount.get_teacher(username=username)
        if data:
            return Response({
            'data': data
            }, status=status.HTTP_200_OK)
        return Response({
            'data':'Teacher not found',
           
        },  status=status.HTTP_400_BAD_REQUEST)

class TeacherDeleteAPIView(APIView):
    def get(self, request, username):
        print('higugifu')
        delete_teacher = TeacherAccount.delete_teacher(username=username)
        print('hiieirhe', delete_teacher)
        if delete_teacher:
            return Response({"success":"Teacher Account delete successfully"}, status=204)
        
        return Response({"failed":"Teacher can not be deleted"}, status=status.HTTP_400_BAD_REQUEST)