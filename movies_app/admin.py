from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Movie, Actor, Genre, CustomUser, Director

# Register your models here.
class CustomUserAdmin(UserAdmin):
  model = CustomUser
  # add_form = CustomUserCreationForm


  fieldsets = (
    *UserAdmin.fieldsets,
    (
      'Additional data',
      {
        'fields': (
          'avatar',
          'bookmarked',

        )
      }
    ),
  )

  add_fieldsets = (
    (None, {'fields': ('username', 'password1', 'password2',
                        'avatar', 'bookmarked',)}),
    )


admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(CustomUser, CustomUserAdmin)