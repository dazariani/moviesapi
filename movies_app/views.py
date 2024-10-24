from http.client import NOT_FOUND
from rest_framework import viewsets, status, mixins
from .serializers import ActorSerializer, GenreSerializer, MovieSerializer, CustomUserSerializer, ChangePasswordSerializer, UpdateBookmarksSerializer, UpdateAvatarSerializer, DirectorSerializer, UpdatePosterSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Actor, Genre, Movie, CustomUser, Director
from django.shortcuts import HttpResponse, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from .permissions import UserModelLevelPermission, UserObjLevelPermission, ModelLevelPermission, ObjectLevelPermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import  DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination






# MyTokenObtainPairView
class MyTokenObtainPairView(TokenObtainPairView):
   serializer_class = MyTokenObtainPairSerializer  


# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
  queryset = Movie.objects.all()
  serializer_class = MovieSerializer
  permission_classes = [ModelLevelPermission, ObjectLevelPermission,]

  def paginate_queryset(self, queryset, view=None):
    if not self.request.query_params:
        return None

    return super().paginate_queryset( queryset)

    # Filtering result
  filter_backends = [OrderingFilter, DjangoFilterBackend]
  ordering_fields = ['year', "rating", ]
  filterset_fields = ['genre__name', ]



class ActorViewSet(viewsets.ModelViewSet):
  queryset = Actor.objects.all()
  serializer_class = ActorSerializer
  permission_classes = [ModelLevelPermission, ObjectLevelPermission,]


class GenreViewSet(viewsets.ModelViewSet):
  queryset = Genre.objects.all()
  serializer_class = GenreSerializer
  permission_classes = [ModelLevelPermission, ObjectLevelPermission,]


class DirectorViewSet(viewsets.ModelViewSet):
  queryset = Director.objects.all()
  serializer_class = DirectorSerializer
  permission_classes = [ModelLevelPermission, ObjectLevelPermission,]


# CustomUser viewSet
class UserViewSet(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
  queryset = CustomUser.objects.all()
  serializer_class = CustomUserSerializer
  permission_classes = [UserModelLevelPermission & UserObjLevelPermission,]

 


# Current user
class UserView(APIView):
    def get(self, request): 
        if not request.user.id:
            raise AuthenticationFailed('Unauthenticated :(')
        
        user = CustomUser.objects.filter(id=request.user.id).first()

        serializer = CustomUserSerializer(user)

        return Response(serializer.data)
    

# Register
class Register(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
          user = serializer.save()
        else:
           return Response(status=status.HTTP_409_CONFLICT) 

        # Add m2m field
        if request.data.get('bookmarked'):
          for movie_id in request.data.get('bookmarked'):
            try:
                movie = Movie.objects.get(id=movie_id)
                print(movie)
                user.bookmarked.add(movie)
                print(user)
            except Movie.DoesNotExist:
                raise NOT_FOUND()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    

# Change password
class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, 
                status=status.HTTP_400_BAD_REQUEST)
            
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Update bookmarked movies
class UpdateBookmarked(GenericAPIView):
   """
   An endpoint for changing bookmarked movies.
   """
   permission_classes = (UserObjLevelPermission, )
   queryset = CustomUser.objects.all()

   def get_object(self):
    obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)
    return obj
   
   def put(self, request, pk):
      self.object = self.get_object()
      user = CustomUser.objects.get(id=pk)
      serializer = UpdateBookmarksSerializer(user, data=request.data)

      if serializer.is_valid():
          serializer.save()

          bookmarked = []
          for movie_id in request.data.get("bookmarked"):
            try:
              movie = Movie.objects.get(id=movie_id)
              bookmarked.append(movie)
            except:
              raise NOT_FOUND()
          
          user.bookmarked.set(bookmarked)  
          return Response(data=serializer.data, status=status.HTTP_200_OK)
        

# Update user avatar
class UpdateAvatar(GenericAPIView):
   """
   An endpoint for changing avatar.
   """
   permission_classes = (UserObjLevelPermission, )
   parser_classes = (MultiPartParser, )
   queryset = CustomUser.objects.all()


   def get_object(self):
    obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)
    return obj
   
   def put(self, request, pk):
      self.object = self.get_object()
      user = CustomUser.objects.get(id=pk)
      serializer = UpdateAvatarSerializer(user, data=request.data)

      if serializer.is_valid():
          serializer.save()

          return Response(data=serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=400)
   

# Update movie poster
class UpdatePoster(GenericAPIView):
   """
   An endpoint for changing avatar.
   """
   permission_classes = (IsAdminUser, )
   parser_classes = (MultiPartParser, )
   queryset = Movie.objects.all()


   def get_object(self):
    obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)
    return obj
   
   def put(self, request, pk):
      self.object = self.get_object()
      user = Movie.objects.get(id=pk)
      serializer = UpdatePosterSerializer(user, data=request.data)

      if serializer.is_valid():
          serializer.save()

          return Response(data=serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=400)

   

        

        
  


