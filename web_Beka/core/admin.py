from django.contrib import admin
from core.models import Films, Comment, Category

# Register your models here.
admin.site.register(Films)
admin.site.register(Comment)
admin.site.register(Category)

