from django.contrib import admin
from .models import User, Comment, Language

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Language)
