from rest_framework import serializers
from .models import Attendance, SchoolUser
from datetime import date, timedelta, datetime
from django.conf import settings
from django.db import transaction



class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'attendance']
    
    @classmethod
    def save_attendance(cls, data):
        """"""
        # with transaction.atomic:
        start_date = settings.TERM_START_DATE
        first_att = '?' * (date.today() - start_date).days
        today = date.today()

        for user_attendance in data:
            try:
                user = Attendance.objects.get(user_id=user_attendance["id"])
                if today >= start_date + timedelta(days=len(user.attendance)):
                    att = user.attendance[:-1]
                else:
                    att = user.attendance
                user.attendance = att + str(user_attendance.attendance)
                user.save()
            except:
                attendance = first_att + str(user_attendance["attendance"])
                user = SchoolUser.objects.get(id=user_attendance["id"])
                Attendance(user=user, attendance=attendance).save()
        return 'Done'
    
    @classmethod
    def get_data(cls, params):
        class_name, user_id, date = params.get('class_name'), params.get('user_id'), params.get('date')
        if date:
            date = datetime.strptime(date, '%y/%m/%d').date()
            data = Attendance.get_attendance_by_day(date, class_name)
        elif user_id:
            data = Attendance.get_dates_absent(user_id)
        else:
            data = Attendance.get_days_absent(class_name)
        return data
