from rest_framework import serializers
from .models import Actor, Genre, Movie, CustomUser, Director
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.filters import OrderingFilter



# My tokenObtain serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
    

class ActorSerializer(serializers.ModelSerializer):
  
  class Meta:    
    model = Actor
    fields = ('name',)  


class DirectorSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Director
    fields = ('name', )    



class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = ('name', )

    
class MovieSerializer(serializers.ModelSerializer):

  # !!! Important part (How to read and write m2m fields) !!!
  actors = ActorSerializer(read_only=True, many=True)
  actors_id = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all(), source='actors', many=True, write_only=True) # Include fields
  genre = GenreSerializer(read_only=True, many=True)
  genre_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), source='genre', many=True, write_only=True) # Include fields

  director = DirectorSerializer(read_only=True, many=True)
  director_id = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all(), source='director', many=True, write_only=True) # Include fields

# No need any more
  # def create(self, validated_data):

  #   # First, remove following from the validated_data dict...
  #   actors_data = validated_data.pop('actors', None)
  #   genre_data = validated_data.pop('genre', None)

  #   print(actors_data, genre_data)

  #   # Set the admin_notes custom value...
  #   # validated_data['admin_notes'] = 'Test'

  #   # Create the object instance...
  #   movie = Movie.objects.create(**validated_data)

  #   # Finally, add your many-to-many relationships...
  #   actors = []
  #   genres = []
  #   if actors_data:
  #       for data1 in actors_data:
  #           a = Actor.objects.filter(id=data1.id).first()
  #           print(a)
  #           actors.append(a.id)
  #           # movie.actors.set(Actor.objects.get(id=data1.id))

  #   if genre_data:
  #       for data2 in genre_data:
  #           g = Genre.objects.filter(id=data2.id).first()
  #           genres.append(g.id)
  #           # movie.genre.set(Genre.objects.get(id=data2.id))
  #   movie.genre.set(genres)       
  #   movie.actors.set(actors)  

  #   return movie

  class Meta:
    model = Movie
    # fields = "__all__"
    fields = ('id', 'title', 
'year',
'genre',
'rating',
'director',
'actors',
'actors_id',
'genre_id',
'director_id',
'poster',
'plot',
'country',
'language',
'url',)



# CustomUser serializer
class CustomUserSerializer(serializers.ModelSerializer):
  bookmarked = MovieSerializer(read_only=True, many=True)

  class Meta:
    model = CustomUser
    fields = ['id', 'username', 'password', 'avatar', 'bookmarked']
    extra_kwargs = {
      'password': {'write_only': True}
    }

# Add m2m field (option for serializer)
  # def create(self, validated_data):
  #   password = validated_data.pop('password', None)
  #   # instance = self.Meta.model(**validated_data)
  #   if self.initial_data['bookmarked']:
  #     movies = self.initial_data['bookmarked']

  #   moviesInstances = []
  #   if movies:
  #     for movie in movies:
  #       moviesInstances.append(Movie.objects.get(pk = movie))
  #     user = CustomUser.objects.create(**validated_data)  
    

  #   if password is not None:
  #     user.set_password(password)
  #     if movies:
  #       user.bookmarked.set(moviesInstances)
  #     user.save()
  #   return user



  def create(self, validated_data):
    # print(self.context["request"].data)
    password = validated_data.pop('password', None)
    instance = self.Meta.model(**validated_data)
    if CustomUser.objects.filter(username=self.context["request"].data["username"]).exists():
      raise serializers.ValidationError("User Already exists.")
    else:
      if password is not None:
        instance.set_password(password)
      instance.save()
      return instance
  


# Change password
class ChangePasswordSerializer(serializers.Serializer):
  """
  Serializer for password change endpoint.
  """
  old_password = serializers.CharField(required=True)
  new_password = serializers.CharField(required=True)

  def validate_new_password(self, value):
      validate_password(value)
      return value
  

# Update user's bookmarked movies
class UpdateBookmarksSerializer(serializers.ModelSerializer):
  bookmarked = MovieSerializer(read_only=True, many=True)

  class Meta:
    model = CustomUser 
    fields = ['bookmarked', ]


# Update user's avatar image
class UpdateAvatarSerializer(serializers.ModelSerializer):
  avatar = serializers.ImageField(required=False)

  class Meta:
    model = CustomUser 
    fields = ['avatar', ]


# Update movie poster
class UpdatePosterSerializer(serializers.ModelSerializer):
  poster = serializers.ImageField(required=False)

  class Meta:
    model = Movie 
    fields = ['poster', ]