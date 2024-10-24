from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, ActorViewSet, GenreViewSet, UserViewSet, MyTokenObtainPairView, UserView, Register, UpdatePassword, UpdateBookmarked, UpdateAvatar, DirectorViewSet, UpdatePoster

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='usersModel')
router.register(r'movies', MovieViewSet, basename='moviesModel')
router.register(r'genres', GenreViewSet, basename='genresModel')
router.register(r'actors', ActorViewSet, basename='actorModel')
router.register(r'director', DirectorViewSet, basename='directorModel')

urlpatterns = [
  path('', include(router.urls)),
  # path('bla', movieTestView),
  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

  path('me', UserView.as_view()),
  path('register', Register.as_view()),
  path('change_password', UpdatePassword.as_view()),
  path('update_bookmarks/<int:pk>', UpdateBookmarked.as_view()),
  path('update_avatar/<int:pk>', UpdateAvatar.as_view()),
  path('update_poster/<int:pk>', UpdatePoster.as_view()),
]


