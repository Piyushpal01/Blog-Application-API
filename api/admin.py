from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Blog

# Register your models here.
# as we have done some changes in default User model & build custom user model so we have to customize the default userAdmin too.
class CustomUserAdmin(UserAdmin):
    list_display=["username", "email", "first_name", "last_name", "job_title", "bio", "profile_pic", "facebook", "youtube", "instagram", "twitter", "linkedin", "github"] 

admin.site.register(CustomUser, CustomUserAdmin)

# Register blog class
class BlogAdmin(admin.ModelAdmin):
    list_display=["title", "author", "is_draft", "category", "created_at"]

admin.site.register(Blog, BlogAdmin)