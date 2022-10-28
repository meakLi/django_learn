from django.db import models
import time


class BaseModel(models.Model):
    # 至少有这两个（偷懒），时间戳，一个整数
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    # auto_now自动处理，填充当前时间，有时区，在调用save（）方法时，时间自动更新
    format_created_at = models.DateTimeField(auto_now=True)
    # 调用更新时，操作，更新时间，auto_now_add时间一直存在不怎么会改变
    format_updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # models.Model中的自带方法，用django就会调用（避免手动更新数据）
        # 取当前的时间戳
        time_now = int(time.time())
        # 数据库的组件，已经被创建，数据已经存在（旧数据）
        if self.pk:
            self.updated_at = time_now
        # 新数据
        else:
            self.created_at = time_now
            self.updated_at = time_now

        # 这里似乎是python2的写法，python3可以直接super().save()
        super(BaseModel, self).save(*args, **kwargs)
        # super().save(*args, **kwargs)

    class Meta:
        # 元类
        # 虚拟类，不会被其他类所继承
        abstract = True
