from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

API_VERSION = 'v1'
app_name = 'api'


router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ResponseViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('token/', views.get_token, name='get_token'),
    path('signup/', views.signup, name='signup'),
]

urlpatterns = [
    path(f'{API_VERSION}/', include(router.urls)),
    path(f'{API_VERSION}/auth/', include(auth_urls)),
]
