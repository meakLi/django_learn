from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from apps.users.models import Users


def get_userinfo(request):
    # pk == 主键 == id
    user = Users.objects.get(id=1)
    # print(user)
    result = render(request, 'userinfo.html', context={
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    })
    return result


def get_users(request):
    # users = Users.objects.all()
    # user_data = []
    # for user in users:
    #     user_data.append({
    #         "id": user.id,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "email": user.email,
    #     })

    print(request)
    if request.method == 'GET':
        # 搜索
        email_query = request.GET.get('email')  # tom
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        users = Users.objects.filter(
            # email__endswith=email_query
            # email精确搜索
            # email__contains包含型筛选
            # email__icontains忽略大小写的非全等
            # email__startwith以..开头
            # email__endwith以..结尾
            # email__istartwith忽略了大小写
            gender__in=[0, 1]  # in 方法，某一个字段是否在列表类
        )
        # 一般不用len，因为可能将数据库中的所有的数据全部导入到python的内存之中，所以使用count方法
        total_count = users.count()  # users查询集，可以理解为列表；
        _users = users[offset:offset + limit]  # 分页操作在数据库层就已经完成，查询出来的数据返回python程序
        # map函数，就是将——users中的每一个元素都进行了函数的操作。
        user_data = list(map(lambda user: {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, _users))

        return JsonResponse({
            "code": 200,
            'message': 'success',
            'data': {
                'list': user_data,
                "pagination": {
                    "total_count": total_count,
                    'offset': offset,
                    "limit": limit,
                }
            }
        })
    else:
        import json
        user_data = json.loads(request.body)

        # 构建数据模型，save
        # user = Users(
        #     first_name=user_data['first_name'],
        #     last_name=user_data['last_name'],
        #     email=user_data['email'],
        #     gender=user_data['gender']
        # )
        # user.save()

        # create方法 ，create方法不需要再save
        user = Users.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            gender=user_data['gender']
        )

        # 创建用户
        return JsonResponse({'code': 200, 'message': 'success', "data": {
            "userId": user.id
        }})
