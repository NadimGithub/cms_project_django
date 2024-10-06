from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from apps.institute.models import InstituteMaster



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, mobile, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        if not mobile:
            raise ValueError('The Mobile field must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, username, email, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(username, email, mobile, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    Role_choices= (
        ('admin', 'Admin'),
        ('principal', 'Principal'),
        ('vice_principal', 'Vice_Principal'),
        ('hod', 'Hod'),
        ('teacher', 'Teacher'),
        ('accountant', 'Accountant'),
        ('clark', 'Clark'),
        ('examinetor', 'Examinetor'),
        ('librarian', 'Librarian'),
        ('lab_assistant', 'Lab_Assistant'),
        ('student', 'student'),
      
        
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=50, unique=True)
    mobile = models.TextField(max_length=10, unique=True)
    email = models.TextField(unique=True)
    address = models.TextField(max_length=100)
    role = models.CharField(max_length=30, choices=Role_choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)  # Typically False for non-superusers
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    inst_id = models.ForeignKey(InstituteMaster,on_delete=models.CASCADE, blank=True, null=True,)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'mobile']

    def __str__(self):
        return self.username
    

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     Role_choices= (
#         ('admin', 'Admin'),
#         ('office', 'Office'),
#         ('principal', 'Principal'),
#         ('hod', 'hod'),
#         ('staff', 'Staff'),
#         ('student', 'Student'),
#         ('parents', 'Parents')
        
#     )

#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     username = models.CharField(max_length=50, unique=True)
#     mobile = models.TextField(max_length=10, unique=True)
#     email = models.TextField(unique=True)
#     address = models.TextField(max_length=100)
#     role = models.CharField(max_length=30, choices=Role_choices)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)  # Typically False for non-superusers
#     profile_image = models.ImageField(upload_to='profile_images/')
#     inst_id = models.IntegerField(blank=True, null=True, default=0)
#     objects = CustomUserManager()

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email', 'mobile']

#     def __str__(self):
#         return self.username
# print(CustomUser,"data print from custome user")


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=255, blank=True, null=True)  # Changed to CharField

    def __str__(self):
        return self.user.username
