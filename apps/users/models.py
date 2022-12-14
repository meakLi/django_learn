from django.db import models
from apps.utils.base_model import BaseModel
from enum import IntEnum


# Create your models here.


class UserGender(IntEnum):
    FEMALE = 0
    MALE = 1
    LADYBOY = 2

    # classmethod 修饰符对应的函数不需要实例化，不需要 self 参数，
    # 但第一个参数需要是表示自身类的 cls 参数，
    # 可以来调用类的属性，类的方法，实例化对象等。
    @classmethod
    def choices(cls):
        return tuple(((item.value, item.name) for item in cls))


class Users(BaseModel):
    # first_name = models.CharField(max_length=200, null=True, blank=True)  # blank 控制admin
    first_name = models.CharField(max_length=200)  # blank 控制admin
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    gender = models.SmallIntegerField(choices=UserGender.choices())

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        # 表名
        db_table = "users"
        # 指定admin显示的名字
        verbose_name_plural = 'users'


class Article(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()  # 没有长度限制
    user = models.ForeignKey(Users, related_name="user_articles", on_delete=models.CASCADE)  # 外键，ForeignKey在那一边就是那边对应多。级联删除
    # SET_NULL 设为null。SET_DEFAULT（1） 设为一个默认值

    class Meta:
        db_table = "articles"
