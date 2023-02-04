from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models, transaction, IntegrityError 
from django.db.models import Count, Prefetch, Sum, Q, F
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from cloudinary.models import CloudinaryField
from django.conf import settings

# from .users.model_mixins import ModelMixin

from .utils import hash_password

# Create your models here.
term_start = settings.TERM_START_DATE

def permission_default():
    return ['staff']

class ModelMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Permission(models.Model):
    per_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    objects = models.Manager()

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Permissions"

    class Admin:
        pass

    def __str__(self):
        return self.name

    @classmethod
    def create_permission(cls, **kwargs):
        permission = cls(**kwargs)
        try:
            permission.save()
            return {"message": "Permission created successfully", "status": True}
        except IntegrityError:
            return {"message": "Permission already exists!", "status": False}

    @classmethod
    def get_permissions(cls):
        permissions = cls.objects.all().values()
        return list(permissions)


class Class(models.Model):
    name = models.CharField(max_length=200)
    section = models.CharField(max_length=200)
    teacher = models.ForeignKey('SchoolUser', on_delete=models.CASCADE, related_name="teacher_class", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
    
    @classmethod
    def create_class(cls, **kwargs):
        teacher_id = kwargs.get("teacher_id")
        if teacher_id:
            teacher = SchoolUser.objects.get(id=teacher_id)
            # print("🚀 ~ file: models.py:74 ~ teacher", teacher)
            if teacher:
                classes = cls.objects.create(teacher=teacher, **kwargs)
            return classes
        return None
    
    @classmethod
    def get_classes(cls):
        query = None
        fields = [
            "id",
            "name",
            # "teacher__first_name",
            # "teacher__last_name",
            # "school_user__middle_name",
            # "school_user__email",
            "section",
            # "state",
            # "country"
        ]
        query = cls.objects.all().values(*fields)
        return list(query)


class SchoolUser(models.Model):
    ROLES = (
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
        ('Parent', 'Parent'),
        ('Staff', 'Staff'),
    )
    GENDER = (
        ("Male", "Male"),
        ("FEMALE", "Female")
    )
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    roles = models.CharField(max_length=200, choices=ROLES, default='Staff')
    gender = models.CharField(max_length=200, choices=GENDER, default='M', null=True, blank=True)
    # permissions = models.JSONField(default=permission_default, blank=True)
    # session_id = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey(
        "SchoolUser", 
        related_name="schooluser_parent",
        on_delete=models.CASCADE,
        blank=True, 
        null=True,
    )
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students', blank=True, 
        null=True,)
    date = models.DateTimeField(default=timezone.now, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['pk']
    

    def __str__(self):
        return f'{self.first_name}- {self.last_name}'
    
    @classmethod
    def create_user(cls, **kwargs):
        with transaction.atomic():
            try:
                pin = kwargs.pop("pin")
                username = kwargs.pop("username")
                image = kwargs.pop("image", None)
                parent = None 
                parent_id = kwargs.pop("parent_id", None)
                class_id = kwargs.pop("class_id", None)
                roles = kwargs.get("roles")
                class_enrolled=None

                if parent_id:
                    parent = cls.get_parent(id=parent_id, obj=True)
                
                if parent and roles == "Student":
                    kwargs.update(
                        parent=parent,
                    )

                if class_id:
                    class_enrolled = cls.get_class(id=class_id, obj=True)

                if class_id and roles == "Student":
                    kwargs.update(
                        class_enrolled=class_enrolled
                    )
                user = cls.objects.create(**kwargs)
                account = Profile.create_profile(
                    username=username,
                    pin=pin,
                    school_user=user,
                    roles=roles,
                    image=image
                )
                if account:
                    return user 
            except IntegrityError as e:
                return {"User" : None, "message":e.args[0]}

    @classmethod
    def get_parent(cls, **kwargs):
        obj = kwargs.pop("obj", None)
        try:
            if obj:
                parent = cls.objects.get(**kwargs)
            else:
                parent = cls.objects.get(**kwargs).values()
        except cls.DoesNotExist:
            parent = None
        return parent
    
    @classmethod
    def get_class(cls, **kwargs):
        obj = kwargs.pop("obj", None)
        try:
            if obj:
                class_id = Class.objects.get(**kwargs)
            else:
                class_id = Class.objects.get(**kwargs).values()
        except cls.DoesNotExist:
            class_id = None
        return class_id
    

class Profile(ModelMixin):
    # TODO : add model mixins later to get created at
    # country = models.CharField(max_length=200)
    # state = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    school_user = models.ForeignKey('SchoolUser',related_name="teacher_user", on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=timezone.now)
    # image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    image = CloudinaryField(blank=True, null=True)
    permissions = models.JSONField(default=permission_default, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    roles = models.CharField(max_length=200, default='Staff', blank=True, null=True)
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
             
    @classmethod
    def create_profile(cls, **kwargs):
        with transaction.atomic():
            try:
                # print(kwargs, 'olol')
                user_account = cls(
                    school_user =kwargs["school_user"],
                    # country=kwargs["country"],
                    username=kwargs["username"],
                    image=kwargs["image"],
                    # state=kwargs["state"]
                   
                )
                user_account.save()
                ProfileLogin.create_login(
                    username = kwargs["username"],
                    permissions = [kwargs["roles"]],
                    pin = kwargs["pin"],
                    profile=user_account,
                    is_first_login=True

                )
                return user_account
            except IntegrityError as e:
                return {"user account":None, "message":e.args[0]}
        
    @classmethod 
    def get_teachers(cls):
        query = None
        fields = [
            "id",
            "username",
            "school_user__first_name",
            "school_user__last_name",
            "school_user__middle_name",
            "school_user__email",
            "school_user__roles",
            # "state",
            # "country"
        ]
        query = cls.objects.filter(school_user__roles="Teacher").values(*fields)
        return list(query)
    
    @classmethod
    def get_teacher_stat(cls):
        now = timezone.now()
        total_teacher_conditions_count = Count(
            "username" #filter=teacheraccount_
        )
        today = Q(added_date__date=now.date())
        yesterday = Q(added_date__date=now.date() - timezone.timedelta(days=1))
        week = Q(added_date__gte=now - timezone.timedelta(days=7))
        month = Q(added_date__gte=now - timezone.timedelta(days=30))
        today_count = Count(
            "username", filter=today
        )
        yesterday_count = Count(
            "username", filter=yesterday
        )

        week_count = Count(
            "username", filter=week
        )

        month_count = Count(
            "username", filter=month
        )
        summary = cls.objects.filter(school_user__roles="Teacher").aggregate(
                        today=today_count,
                        yesterday=yesterday_count,
                        week=week_count,
                        month=month_count,
                        total=total_teacher_conditions_count
                    )

        return summary

    @classmethod
    def get_parents(cls):
        query = None
        fields = [
            "id",
            "username",
            "school_user__first_name",
            "school_user__last_name",
            "school_user__middle_name",
            "school_user__email",
            "school_user__roles",
            # "state",
            # "country"
        ]
        query = cls.objects.filter(school_user__roles="Parent").values(*fields)
        return list(query)
    
    
    @classmethod
    def get_students(cls):
        query = None
        fields = [
            "id",
            "username",
            "school_user__first_name",
            "school_user__last_name",
            "school_user__middle_name",
            "school_user__email",
            "school_user__roles",
            # "state",
            # "country"
        ]
        query = cls.objects.filter(school_user__roles="Student").values(*fields)
        return list(query)



class ProfileLogin(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    pin = models.CharField(max_length=200, blank=True, null=True)
    is_first_login = models.BooleanField(default=False)  # awaiting first login
    status = models.BooleanField(default=True)
    # session_id = models.CharField(max_length=255, null=True, blank=True)
    session_id = models.UUIDField(null=True, blank=True)
    permissions = models.JSONField(default=permission_default, blank=True)
    perms = models.ForeignKey
    # student_account = models.OneToOneField(StudentAccount, on_delete=models.CASCADE, related_name='profile_login', null=True, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile_login', null=True, blank=True)
    password_reset_pin = models.CharField(max_length=255, null=True, blank=True)
    password_reset_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.username}'

    @classmethod
    def create_login(cls, **kwargs):
        # print("LOGIN", kwargs)
        kwargs["pin"] = hash_password(kwargs["pin"])
        cls(**kwargs).save()
    

class Subject(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ForeignKey(SchoolUser, on_delete=models.SET_NULL, null=True, blank=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

class Grade(models.Model):
    student = models.ForeignKey(SchoolUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

# class Attendance(models.Model):
#     student = models.ForeignKey(SchoolUser, on_delete=models.CASCADE)
#     class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     date = models.DateField()
#     present = models.BooleanField(default=False)

class Attendance(models.Model):
    user = models.ForeignKey(SchoolUser, on_delete=models.CASCADE)
    attendance = models.CharField(max_length=150)
    objects = models.Manager

    def get_dates_absent(self):
        att = self.attendance
        return [str(term_start + timedelta(days=i)) for i, at in enumerate(list(att)) if at == '0']

    @classmethod
    def get_days_absent(cls, class_name):
        students = cls.objects.filter(user__class_enrolled__name=class_name)
        return {student.user_id:student.get_dates_absent() for student in list(students)}

