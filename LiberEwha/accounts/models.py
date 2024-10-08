from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    nickname = models.CharField(max_length=10, unique=True)
    is_tf = models.BooleanField(default=False, null=True)
    is_admin = models.BooleanField(default=False, null=True)
    is_show = models.BooleanField(default=False, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.nickname
