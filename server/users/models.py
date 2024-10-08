from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsersManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class Users(AbstractUser):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('verified', 'Verified'),
        ('vip', 'VIP'),
        ('blocked', 'Blocked'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    username = None
    
        
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    objects = UsersManager()
    
    email = models.EmailField(unique=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    serializer_class = 'users.serializers.AppUsersSerializer';
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
