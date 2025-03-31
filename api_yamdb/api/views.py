import random

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (
    IsAdmin,
)
from .serializers import (
    MeUserSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer
)
from users.models import User


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        return Response(
            'Такие "username" или "e-mail" уже существуют',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Confirmation code',
        f'Code: {user.confirmation_code}',
        settings.EMAIL_HOST,
        [serializer.validated_data.get('email')]
    )
    return Response(
        serializer.data, status=status.HTTP_200_OK
    )


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
    return Response(
        'Неверный код подтверждения', status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        ['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(
            User,
            pk=request.user.id
        )
        if request.method == 'PATCH':
            serializer = MeUserSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = MeUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
