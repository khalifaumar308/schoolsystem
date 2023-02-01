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



# class CustomUserManager(BaseUserManager):
    

    def create_superuser(self, email, username, password,first_name, last_name,  **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        # other_fields.setdefault('first_name', None)
        # other_fields.setdefault('last_name', None)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'superuser must be assigned to is_staff=True'
            )
        
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError(
#                 'superuser must be assigned to is_superuser=True'
#             )
        
#         return self.create_user(email, username, first_name, last_name, password, **other_fields)


# class NewUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(_('email address'), unique=True)
#     username = models.CharField(max_length=200, unique=True)
#     first_name = models.CharField(max_length=200, blank=True)
#     last_name = models.CharField(max_length=200, blank=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)


#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#     objects = CustomUserManager()

#     def __str__(self):
#         return f"{self.email}"


class UserAccount(models.Model):
    pass 


class OtherUser(models.Model):
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
    email = models.EmailField(max_length=255, null=True)
    roles = models.CharField(max_length=200, choices=ROLES, default='Staff')
    gender = models.CharField(max_length=200, choices=GENDER, default='M', null=True, blank=True)
    permissions = models.JSONField(default=permission_default, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['pk']
    

    def __str__(self):
        return f'{self.first_name}- {self.last_name}'


    @classmethod
    def create_other_useraccount(cls, **kwargs):
        with transaction.atomic():
            try:
                roles = kwargs.get("roles", None)
                pin = kwargs.pop('pin')
                username = kwargs.pop('username')
                other_user = cls.objects.create(**kwargs)
                if roles == "Teacher":
                    teacher = TeacherAccount.create_account(
                        username=username,
                        state=kwargs["state"],
                        country=kwargs["country"],
                        roles="teacher",
                        pin = pin,
                        other_user=other_user,
                    )
                    return other_user
                else:
                    transaction.set_rollback(True)
                    return None
            except IntegrityError as e:
                return {"Other User" : None, "message":e.args[0]}


class TeacherAccount(models.Model):
    # first_name = models.CharField(max_length=200)
    # middle_name = models.CharField(max_length=200)
    # last_name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    other_user = models.ForeignKey('OtherUser',related_name="teacher_user", on_delete=models.CASCADE)
    # email = models.EmailField(max_length=255, null=True)

    @classmethod
    def create_account(cls, **kwargs):
        with transaction.atomic():
            try:
                teacheraccount = cls(
                    other_user =kwargs["other_user"],
                    country=kwargs["country"],
                    username=kwargs["username"],
                    state=kwargs["state"]
                   
                )
                teacheraccount.save()
                ProfileLogin.create_login(
                    username = kwargs["username"],
                    pin = kwargs["pin"],
                    teacher_account=teacheraccount,
                    is_first_login=True

                )
                return teacheraccount
            except IntegrityError as e:
                return {"teacher account":None, "message":e.args[0]}


    @classmethod
    def get_teachers(cls):
        query = None
        query = cls.objects.values(
                "id",
                "username",
                "other_user__first_name",
                "other_user__last_name",
                "other_user__middle_name",
                "other_user__email",
                "other_user__roles",
                "state",
                "country"

        )
        return list(query)
    
    @classmethod
    def delete_teacher(cls, username):
        teacher = TeacherAccount.objects.filter(username=username)
        if teacher:
            teacher.delete()
            return True
        else:
            return False
    
    # @classmethod
    # def deactivate_teacher(cls, username):
    #     teacher = TeacherAccount.objects.get(username=username)
    #     teacher.is_active = False 
    #     teacher.save()
    
    @classmethod
    def get_teacher(cls, username):
        query = None
        try:
            query = cls.objects.filter(username=username).values(
                "username",
                "other_user__first_name",
                "other_user__last_name",
                "other_user__middle_name",
                "other_user__email",
                "other_user__roles",
                "state",
                "country"

            )
            return query
        except cls.DoesNotExist:
            return 'Not Found'


    @classmethod
    def update_teacher(cls, username, **kwargs):
        query = cls.objects.filter(username=username).update(**kwargs)
        if query:
            return {"status":True, "message":"update successfully"}
        return {"status":False, "message":"update Failed"}
         

    @classmethod
    def total_teachers(cls, conditions):
        # teacher_conditions  = Q(teacheraccount__other_user_created_at__lte=conditions)
        total_teacher_conditions_count = Count(
            "username" #filter=teacheraccount_
        )
        teacher_summaries = cls.objects.aggregate(
            total_teachers=total_teacher_conditions_count
        )

        return teacher_summaries
    
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
        summary = cls.objects.aggregate(
            today=today_count,
            yesterday=yesterday_count,
            week=week_count,
            month=month_count,
            total=total_teacher_conditions_count
        )

        return summary
    
    @classmethod
    def percentage_new_teachers_per_month(cls):
        now = datetime.now()
        month = now.month
        year = now.year
        print(f"month: {month} year:{year}")
        start_date = timezone.make_aware(timezone.datetime(year, month, 1))
        end_date = start_date + timedelta(days=31)
        new_teachers = cls.objects.filter(added_date__range=(start_date, end_date)).count()
        total_teachers = cls.objects.all().count()
        if total_teachers == 0:
            return 0
        else:
            return (new_teachers / total_teachers) * 100
    


    def other_user_value(self):
        return f'{self.other_user.first_name} {self.other_user.last_name}'
    

    def __str__(self):
        return f'{self.username}-{self.state}'


class ProfileLogin(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    pin = models.CharField(max_length=200, blank=True, null=True)
    is_first_login = models.BooleanField(default=False)  # awaiting first login
    status = models.BooleanField(default=True)
    # session_id = models.CharField(max_length=255, null=True, blank=True)
    session_id = models.UUIDField(null=True, blank=True)
    permissions = models.JSONField(default=permission_default, blank=True)
    # student_account = models.OneToOneField(StudentAccount, on_delete=models.CASCADE, related_name='profile_login', null=True, blank=True)
    teacher_account = models.OneToOneField(TeacherAccount, on_delete=models.CASCADE, related_name='profile_login', null=True, blank=True)
    password_reset_pin = models.CharField(max_length=255, null=True, blank=True)
    password_reset_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.username}'

    @classmethod
    def create_login(cls, **kwargs):
        kwargs["pin"] = hash_password(kwargs["pin"])
        cls(**kwargs).save()
    
    @classmethod
    def login(cls, request, username=None, password=None):
        try:
            user = cls.objects.get(username=username)
            request.session["username"] = username
            if user.password_reset_pin:
                if user.password_reset_pin == hash_password(password):
                    url  = "/user/password_reset"
                    return {"status":True, "url":url}
                else:
                    return {"status":False, "message" : "wrong otp"}
            elif user.pin and user.is_first_login:
                if user.pin == hash_password(password):
                    url = "/user/change_password"
                    return {"status":True, "url":url}
                else:
                    message = "Your OTP is wrong."
                    return {"status": False, "message": message}
            else:
                if user:
                    if user.password == hash_password(password):
                        url = "/dashboard/"
                        return {"status": True, "url":url}
                    else:
                        message = "incorrect password"
                        return {"status":False, "message":message}
        
        except cls.DoesNotExist:
            message = "Username is incorrect."
            return {"status": False, "message": message}





# class Otherz(User):
#     GENDER_CHOICES = (
#         ("Male", "M"),
#         ("Female", "F"),
#     )
#     gender = models.CharField(max_length=200, choices=GENDER_CHOICES, default='M', null=True, blank=True)
#     permissions = models.JSONField(default={}, blank=True)
#     session_id = models.UUIDField(null=True, blank=True)
#     date = models.DateTimeField(auto_now_add=True)

#     @classmethod
#     def create_other_useraccount(cls, **kwargs):
#         with transaction.atomic():
#             try:
#                 roles = kwargs.pop('roles')
#                 pin = kwargs.pop('pin')
#                 username = kwargs.pop('username')
#                 email = kwargs.pop('email')
#                 password = kwargs.pop('password')
#                 user = cls.objects.create_user(username=username, email=email, password=password)
#                 user.first_name = kwargs.get('first_name')
#                 user.last_name = kwargs.get('last_name')
#                 user.middle_name = kwargs.get('middle_name')
#                 user.save()
#                 if roles == "Teacher":
#                     group = Group.objects.get(name='Teacher')
#                     user.groups.add(group)
#                 elif roles == "Student":
#                     group = Group.objects.get(name='Student')
#                     user.groups.add(group)
#                     user.save()
#                 return user
#             except Exception as e:
#                 raise e

# class Profiles(ModelMixin):
#     username = models.CharField(max_length=200, unique=True)
#     user = models.OneToOneField(OtherUser, on_delete=models.CASCADE)
#     pin = models.CharField(max_length=200, null=True, blank=True)
#     dob = models.DateField(null=True, blank=True)
#     address = models.CharField(max_length=200, null=True, blank=True)
#     phone = models.CharField(max_length=200, null=True, blank=True)
#     bio = models.TextField(null=True, blank=True)
#     avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)

#     def create_profile(sender, instance, created, **kwargs):
#         if created:
#             Profiles.objects.create(user=instance)

#     models.signals.post_save.connect(create_profile, sender=OtherUser)


# class ProfileLogin(models.Model):
#     username = models.CharField(max_length=200, unique=True)
#     password = models.CharField(max_length=200, blank=True, null=True)
#     pin = models.CharField(max_length=200, blank=True, null=True)
#     is_first_login = models.BooleanField(default=False)  # awaiting first login
#     status = models.BooleanField(default=True)
#     session_id = models.CharField(max_length=255, null=True, blank=True)
#     profile = models.OneToOneField(Profiles, on_delete=models.CASCADE, related_name='profile_login', null=True, blank=True)
#     # student_account = models.OneToOneField(StudentAccount, on_delete=models.CASCADE, related_name='profile_login', null=True, blank=True)
#     # teacher_account = models.OneToOneField(TeacherAccount, on_delete=models.CASCADE, related_name='profile_login', null=True, blank=True)

#     def __str__(self):
#         return f'{self.username}'
    
#     @receiver(post_save, sender=Profiles)
#     def create_profile_login(sender, instance, created, **kwargs):
#         if created:
#             pin = instance.pin
#             hashed_pin = hash_password(pin)
#             ProfileLogin.objects.create(username=instance.user.username, pin=hashed_pin, profile=instance)

#     @classmethod
#     def create_login(cls, **kwargs):
#         kwargs["pin"] = hash_password(kwargs["pin"])
#         cls(**kwargs).save()
