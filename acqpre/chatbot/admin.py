from django.contrib import admin

from .models import Tag, Response, Pattern

# Register your models here.
admin.site.register(Tag)
admin.site.register(Response)
admin.site.register(Pattern)
