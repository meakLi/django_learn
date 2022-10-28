from django.db import models
import time


class BaseModel(models.Model):
    # 至少有这两个（偷懒）
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    # auto_now自动处理，填充当前时间
    format_created_at = models.DateTimeField(auto_now=True)
    # 调用更新时，操作，更新时间
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

        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        # 元类
        # 虚拟类，被其他所继承
        abstract = True