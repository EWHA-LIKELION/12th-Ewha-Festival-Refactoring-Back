from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'nickname', 'is_tf', 'is_admin']
        extra_kwargs = {'password': {'write_only': True}}  # 비밀번호는 출력되지 않도록 설정

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            is_tf=validated_data.get('is_tf', False),
            is_admin=validated_data.get('is_admin', False),
        )
        user.set_password(validated_data['password'])  # 비밀번호 설정
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('사용자가 존재하지 않습니다.')

        if not user.check_password(password):
            raise serializers.ValidationError('잘못된 비밀번호입니다.')

        # 토큰 생성
        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'access_token': access,
            'refresh_token': refresh,
            'is_tf': user.is_tf,
            'is_admin': user.is_admin,
        }

        return data
