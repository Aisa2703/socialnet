from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Short)
admin.site.register(SavedPost)
admin.site.register(Notification)