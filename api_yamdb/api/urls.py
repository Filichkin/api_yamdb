from django.urls import include, path
from rest_framework import routers

from . import views


API_VERSION = 'v1'

app_name = 'api'

router = routers.DefaultRouter()

router.register('users', views.UserViewSet, basename='users')
router.register('categories', views.CategoriesViewSet, basename='categories')
router.register('genres', views.GenreVeiwset, basename='genres')
router.register('titles', views.UserViewSet, basename='titles')


auth_urls = [
    path('token/', views.get_token, name='get_token'),
    path('signup/', views.signup, name='signup')
]

urlpatterns = [
    path(f'{API_VERSION}/', include(router.urls)),
    path(f'{API_VERSION}/auth/', include(auth_urls)),
]
