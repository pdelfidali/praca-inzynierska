from django.contrib import admin
from django.db.models import Avg

from .models import Tag, Response, Pattern, Rating


# Register your models here.
class ResponseInLine(admin.StackedInline):
    model = Response
    can_delete = False
    min_num = 1
    max_num = 1


class PatternInLine(admin.StackedInline):
    model = Pattern
    extra = 1


class TagAdmin(admin.ModelAdmin):
    inlines = [ResponseInLine, PatternInLine, ]
    search_fields = ['name']
    list_display = ['name', 'amount']
    sortable_by = ['amount']


class PatternAdmin(admin.ModelAdmin):
    list_display = ['text', 'tag']
    list_editable = ['tag']
    list_filter = ['tag']
    autocomplete_fields = ['tag']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['get_tag', 'rating', 'ip']

    def has_add_permission(self, request):
        return False

    @admin.display(description='Tag')
    def get_tag(self, obj):
        return obj.response.tag


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['tag', 'legal_basis', 'source', 'moderator', 'legal_status_as_of', 'last_edit', 'rating_avg',
                    'rating_no']
    list_filter = ['moderator', 'last_edit', 'legal_status_as_of']
    readonly_fields = ['last_edit']
    search_fields = ['tag__name', 'legal_basis']

    @admin.display(description='Ilość ocen')
    def rating_no(self, obj):
        return Rating.objects.filter(response=obj).count()

    @admin.display(description='Średnia ocen')
    def rating_avg(self, obj):
        ratings = Rating.objects.filter(response=obj).aggregate(Avg('rating'))['rating__avg']
        if not ratings:
            return '-'
        return ratings


admin.site.register(Tag, TagAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Rating, RatingAdmin)
