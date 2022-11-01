from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from apps.users.models import Users
import json
import time
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.serializers import CreateUserSerializer, UserModelSerializer


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

    # print(request)
    # import logging
    # logger = logging.getLogger("errmsg")  # 注意日志处理器的级别
    # logger.info("info log")  # 级别低了记录不了
    # logger.error("error log")
    if request.method == 'GET':
        # 搜索
        email_query = request.GET.get('email')  # tom
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        users = Users.objects.filter(
            email__endswith=email_query
            # email精确搜索
            # email__contains包含型筛选
            # email__icontains忽略大小写的非全等
            # email__startwith以..开头
            # email__endwith以..结尾
            # email__istartwith忽略了大小写
            # gender__in=[0, 1]  # in 方法，某一个字段是否在列表类
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


class UsersView(APIView):

    def get(self, request):
        email_query = request.GET.get('email')  # tom
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        users = Users.objects.filter(
            email__endswith=email_query
            # gender__in=[0, 2]
        )
        total_count = users.count()  # users查询集，可以理解为列表；
        _users = users[offset:offset + limit]  # 分页操作在数据库层就已经完成，查询出来的数据返回python程序
        # map函数，就是将——users中的每一个元素都进行了函数的操作。
        user_data = UserModelSerializer(_users, many=True).data
        # user_data = list(map(lambda user: {
        #     "id": user.id,
        #     "first_name": user.first_name,
        #     "last_name": user.last_name,
        #     "email": user.email,
        # }, _users))
        return Response(
            {
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
            }
        )

    def post(self, request):
        user_data = json.loads(request.body)
        serializers = CreateUserSerializer(data={
            "email": user_data.get("email"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "gender": user_data.get("gender"),
        })

        # if not serializers.is_valid():
        if not serializers.is_valid():
            return Response(serializers.error)

        _user = Users.objects.filter(email=user_data['email']).first()
        if _user:
            return Response({"code": 404})

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


class UserLoginView(APIView):
    # 不做校验，只针对这一个接口
    authentication_classes = ()

    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        user = Users.objects.filter(email=email).first()
        if not user:
            return Response({'code': 404, 'message': 'Not Found'})

        payload = {
            "email": email,
            "exp": int(time.time()) + 30 * 60,
        }
        # 引入settings导入
        from django.conf import settings
        import jwt
        secret_key = settings.SECRET_KEY
        # encode编码，加密方法
        token = jwt.encode(payload, secret_key, algorithm='HS256').decode("utf-8")

        return Response({
            'code': 200,
            'message': 'success',
            'data': {
                'token': token
            }
        })
