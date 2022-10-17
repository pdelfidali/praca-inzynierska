from django.contrib import admin

from .models import Tag, Response, Pattern, Rating

# Register your models here.
class ResponseInLine(admin.StackedInline):
    model = Response
    can_delete = False
    min_num = 1
    max_num = 1


class PatternInLine(admin.StackedInline):
    model = Pattern
    extra = 2
    min_num = 1


class TagAdmin(admin.ModelAdmin):
    inlines = [ResponseInLine, PatternInLine, ]


admin.site.register(Tag, TagAdmin)
admin.site.register(Response)
admin.site.register(Pattern)
admin.site.register(Rating)
