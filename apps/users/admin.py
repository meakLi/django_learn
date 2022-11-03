from django.contrib import admin
from apps.users.models import Users, Article
from django.contrib.auth.models import User, Group

# Register your models here.
# admin.site.register(Users)
# 不显示
admin.site.unregister(Group)
admin.site.unregister(User)
# admin.site.register(Article)


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    # fields = ['first_name', 'last_name', 'email']
    exclude = ['created_at', 'updated_at']
    list_display = ['id', 'first_name', 'last_name', 'email', 'gender']  # 列表页
    search_fields = ['first_name']  # 搜索
    list_filter = ['gender']
    actions = ['change_name']

    def change_name(self, request, queryset):  # 请求，查询集（你选择了那些元素）
        for item in queryset:
            item.first_name = 'sb'
            item.save()
            print(item)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # fields = ['first_name', 'last_name', 'email']
    exclude = ['created_at', 'updated_at']
    list_display = ['title', 'user']  # 列表页
    search_fields = ['user']  # 搜索
    list_filter = ['user']