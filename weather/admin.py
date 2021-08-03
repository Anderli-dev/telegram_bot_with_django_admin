from django.contrib import admin
from weather.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
