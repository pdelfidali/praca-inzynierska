from django.contrib import admin
from django.db.models import Avg
from django.http import HttpRequest

from .models import Tag, Response, Pattern, Rating, Report


# Register your models here.
class TagInLine(admin.StackedInline):
    model = Tag


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
    list_display = ['text', 'tag', 'timestamp']
    list_editable = ['tag']
    list_filter = ['tag']
    autocomplete_fields = ['tag']
    readonly_fields = ['timestamp']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['get_tag', 'rating', 'ip']

    def has_add_permission(self, request):
        return False

    @admin.display(description='Tag')
    def get_tag(self, obj):
        return obj.response.tag


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['tag', 'response_status', 'legal_basis', 'source', 'moderator', 'legal_status_as_of', 'last_edit',
                    'rating_avg', 'rating_no']
    list_filter = ['moderator', 'response_status']
    search_fields = ['tag__name', 'legal_basis']

    def get_readonly_fields(self, request: HttpRequest, obj=None):
        if request.user.is_superuser:
            return ['last_edit']
        elif obj.moderator == request.user:
            return ['moderator', 'response_status', 'last_edit']
        else:
            return ['tag', 'text', 'legal_basis', 'source', 'moderator', 'response_status', 'legal_status_as_of',
                    'last_edit']

    def save_model(self, request, obj: Response, form, change):
        if not request.user.is_superuser:
            obj.response_status = Response.FIXED
            obj.moderator = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='Ilość ocen')
    def rating_no(self, obj):
        return Rating.objects.filter(response=obj).count()

    @admin.display(description='Średnia ocen')
    def rating_avg(self, obj):
        ratings = Rating.objects.filter(response=obj).aggregate(Avg('rating'))['rating__avg']
        if not ratings:
            return '-'
        return ratings


class ReportAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'tag', 'category', 'text', 'response']
    list_filter = ['category']
    search_fields = ['tag', 'response']
    sortable_by = ['timestamp', 'tag']


admin.site.register(Tag, TagAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Report, ReportAdmin)
