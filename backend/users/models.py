from django.db import models, transaction, IntegrityError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from .utils import hash_password

# Create your models here.


class CustomUserManager(BaseUserManager):

    def create_user(self, email,  username, first_name=None, last_name=None, password=None, **other_fields):
        if not username:
            raise ValueError('Users must have an username')
        
        if not email:
            raise ValueError('Must provide an email address')

        email=self.normalize_email(email)
        user = self.model(
            username=username, 
            email=email,
            first_name=first_name,
            last_name=last_name,
            **other_fields
        )

        user.set_password(password)
        user.save(using=self.db)
        return user 
    

    def create_superuser(self, email, username, password,first_name, last_name,  **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'superuser must be assigned to is_staff=True'
            )
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'superuser must be assigned to is_superuser=True'
            )
        
        return self.create_user(email, username, first_name, last_name, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"


class UserAccount(models.Model):
    pass 


class OtherUser(models.Model):
    ROLES = (
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
        ('Parent', 'Parent'),
        ('Staff', 'Staff'),
    )
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255, null=True)
    roles = models.CharField(max_length=200, choices=ROLES, default='Staff')



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
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    other_user = models.ForeignKey('OtherUser',related_name="teacher_user", on_delete=models.CASCADE)

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
        query = cls.objects.all()
        return query
    
    @classmethod
    def delete_teacher(cls, username):
        teacher = TeacherAccount.objects.filter(username=username)
        if teacher:
            teacher.delete()
            return True
        else:
            return False
    
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
    session_id = models.CharField(max_length=255, null=True, blank=True)
    # student_account = models.OneToOneField(StudentAccount, on_delete=models.CASCADE, related_name='profile_login', null=True, blank=True)
    teacher_account = models.OneToOneField(TeacherAccount, on_delete=models.CASCADE, related_name='profile_login', null=True, blank=True)

    def __str__(self):
        return f'{self.username}'

    @classmethod
    def create_login(cls, **kwargs):
        kwargs["pin"] = hash_password(kwargs["pin"])
        cls(**kwargs).save()

