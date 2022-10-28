from django.db import models
from apps.utils.base_model import BaseModel
from enum import IntEnum


# Create your models here.


class UserGender(IntEnum):
    FEMALE = 0
    MALE = 1
    LADYBOY = 2

    @classmethod
    def choices(cls):
        return tuple(((item.value, item.name) for item in cls))


class Users(BaseModel):
    first_name = models.CharField(max_length=200, null=True, blank=True)  # blank 控制admin
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    gender = models.SmallIntegerField(choices=UserGender.choices())

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        # 表名
        db_table = "users"
        # 指定显示的名字
        verbose_name_plural = 'users'
