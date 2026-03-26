from django.contrib import admin
from django.contrib.auth.models import User
from .models import Channel, Group

from .models import Profile, Post

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Channel)
admin.site.register(Post)
