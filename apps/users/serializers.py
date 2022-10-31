# 序列化
from rest_framework import serializers
from apps.users.models import UserGender,Users


class CreateUserSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=200)
    first_name = serializers.CharField(max_length=200, error_messages={'blank': 'first name is required.'})
    last_name = serializers.CharField(max_length=200)
    gender = serializers.ChoiceField(choices=[])

    def validate(self, attrs):
        email = attrs.get('email')
        if Users.objects.filter(email=email).exists():
            raise serializers.ValidationError("User already exists.")

        return attrs


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        # 模型
        model = Users
        # 解析那些字段
        fields = '__all__'
        # fields = ['id']
        # exclude =['id']