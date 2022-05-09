import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def get_or_create(self, iin, name=None):
        if not iin:
            raise ValueError("Users Must Have an iin")
        try:
            user = User.objects.get(
                iin=iin
            )
        except Exception as e:
            print(e)
            user = User.objects.create(
                iin=iin,
                name=name
            )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    iin = models.TextField(max_length=255, unique=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    keystore = models.CharField(max_length=5000, null=True, blank=True)

    email = models.EmailField('Электронная почта', null=True, blank=True)
    degree = models.TextField(null=True, blank=True)
    job_title = models.TextField(null=True, blank=True)

    USERNAME_FIELD = "iin"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.iin

    class Meta:
        db_table = "login"