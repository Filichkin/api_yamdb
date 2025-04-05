from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitlesFilter
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrModeratorOrAdmin
)
from reviews.models import Category, Genre, Review, Title
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    TokenSerializer,
    UserSerializer
)
from users.models import User


@api_view(['POST'])
def signup(request):
    """
    Позволяет получить код подтверждения на переданный email.
    Обрабатывает запрос для эндпоинта api/v1/auth/signup.
    """
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        serializer.validated_data, status=status.HTTP_200_OK
    )


@api_view(['POST'])
def get_token(request):
    """
    Позволяет получть JWT-токен в обмен на username и confirmation code.
    Обрабатывает запрос для эндпоинта api/v1/auth/token.
    """
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    token = {'token': str(AccessToken.for_user(user))}
    return Response(token, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    Обрабатывает все запросы для эндпоинта api/v1/users/.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('^username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        ['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def user_own_account(self, request):
        """
        Позволяет получить и изменить данные своей учетной записи.
        Обрабатывает все запросы для эндпоинта api/v1/me/.
        """
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BaseCategoryGenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Базовый класс категорий и жанров.
    """

    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(BaseCategoryGenreViewSet):
    """
    Позволяет получить список, создать или удалить категорию.
    Обрабатывает все запросы для эндпоинта api/v1/categories/.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseCategoryGenreViewSet):
    """
    Выполняет все операции с жанрами.
    Обрабатывает все запросы для эндпоинта api/v1/genres/.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """Выполняет все операции с произведениями.
    Обрабатывает все запросы для эндпоинта api/v1/titles/.
    """

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).select_related('category').order_by('category__name', '-rating')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update'}:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Выполняет все операции с отзывами.
    Обрабатывает запросы 'get', 'post', 'patch', 'delete'
    для эндпоинта api/v1/titles/{title_id}/reviews.
    """

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdmin
    )
    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.select_related(
            'author').order_by('pub_date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Выполняет все операции с комментариями.
    Обрабатывает запросы 'get', 'post', 'patch', 'delete' для
    эндпоинта api/v1/titles/{title_id}/reviews/{review_id}/comments.
    """

    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin
    )
    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_review(self):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        return get_object_or_404(Review, pk=review_id, title_id=title_id)

    def get_queryset(self):
        return self.get_review().comments.order_by('pub_date')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
