from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models, transaction, IntegrityError 
from django.db.models import Count, Prefetch, Sum, Q, F
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings

# from .users.model_mixins import ModelMixin

from .utils import hash_password

# Create your models here.

def permission_default():
    return ['staff']


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
        ("Male", "M"),
        ("FEMALE", "F")
    )
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    # add gender male or female
    # email = models.EmailField(max_length=255, null=True)
    roles = models.CharField(max_length=200, choices=ROLES, default='Staff')
    # gender = models.CharField(max_length=200, choices=GENDER, default='M', null=True, blank=True)
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
                # pin = kwargs.pop("pin")
                parent = None 
                parent_id = kwargs.pop("parent_id", None)

                if parent_id:
                    parent = cls.get_parent(id=parent_id, obj=True)
                
                if parent:
                    kwargs.update(
                        parent=parent,
                    )
                schooluser = cls.objects.create(**kwargs)
                print("GETTER")
                print(schooluser)
            except IntegrityError as e:
                return {"Other User" : None, "message":e.args[0]}

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


class Attendance(models.Model):
    user = models.ForeignKey(SchoolUser, on_delete=models.CASCADE)
    attendance = models.CharField(max_length=150)
    
    def get_dates_absent(self):
        term_start = settings.TERM_START_DATE
        att = self.attendance
        return [term_start + timedelta(days=i) for i, at in enumerate(list(att)) if at == '0']

