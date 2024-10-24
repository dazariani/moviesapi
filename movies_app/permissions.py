from rest_framework import permissions
from .models import Actor, Movie, Genre, CustomUser

# User permissions
class UserObjLevelPermission(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):

    if request.user.is_staff:
      return True
    elif request.user.id == obj.id:
      return True
    else:
      return False
    
    
class UserModelLevelPermission(permissions.BasePermission):

  def has_permission(self, request, view):

    if not request.user.is_staff and request.method == "PUT":
      return True
    return False
  

# Movie permissions
class ObjectLevelPermission(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    print("From movie object level")

    if request.method in permissions.SAFE_METHODS:
      return True
    if request.user.is_staff:
      return True
    return False 
    

class ModelLevelPermission(permissions.BasePermission):
  print("From movie model level")

  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    
    if request.user.is_staff:
      return True
    return False
    
    