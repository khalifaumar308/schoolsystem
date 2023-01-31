from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models, transaction, IntegrityError 
from django.db.models import Count, Prefetch, Sum, Q, F
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# from .users.model_mixins import ModelMixin

from .utils import hash_password

# Create your models here.

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
                parent = None 
                parent_id = kwargs.pop("parent_id", None)
                roles = kwargs.get("roles")

                if parent_id:
                    parent = cls.get_parent(id=parent_id, obj=True)
                
                if parent and roles == "Student":
                    kwargs.update(
                        parent=parent,
                    )
                user = cls.objects.create(**kwargs)
                account = Profile.create_profile(
                    username=username,
                    pin=pin,
                    school_user=user,
                    roles=roles
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
    

class Profile(ModelMixin):
    # TODO : add model mixins later to get created at
    # country = models.CharField(max_length=200)
    # state = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    school_user = models.ForeignKey('SchoolUser',related_name="teacher_user", on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
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
    
