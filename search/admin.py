from django.contrib import admin
from .models import Mpolynom

# Register your models here.
# diplay mpolynom on the admin page
#admin.site.unregister(Mpolynom)

class MpolynomAdmin(admin.ModelAdmin):
    # non-superuser users can change only their inputs
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    def save_model(self, request, obj, form, change):
        obj.author = request.user.username
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            if obj and obj.status == 'approved':
                return self.readonly_fields + ('mpolynomyal', 'structure_name', 'Mid', 'author','published_recently', 'status', 'keywords', 'comments', 'references', 'links')
            return self.readonly_fields + ('status',)
        return self.readonly_fields


    # def changelist_view(self, request, extra_context=None):    
    #     if not request.user.is_superuser:
    #         self.list_display = ('mpolynomyal', 'structure_name', 'Mid', 'author','published_recently')
    #     else:
    #         self.list_display = ('mpolynomyal', 'structure_name', 'Mid', 'author','published_recently', 'status')
    #     return super(MyAdmin, self).changelist_view(request, extra_context)
    list_display = ('mpolynomyal', 'structure_name', 'Mid', 'author','published_recently', 'status')
    list_filter = ['publication_date']
    search_fields = ['mpolynomyal', 'structure_name','author','Mid']
admin.site.register(Mpolynom, MpolynomAdmin)