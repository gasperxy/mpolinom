from django.contrib import admin
from .models import Mpolynom

# Register your models here.
# diplay mpolynom on the admin page
#admin.site.unregister(Mpolynom)

class MpolynomAdmin(admin.ModelAdmin):
    list_display = ('mpolynomyal', 'structure_name', 'Mid', 'published_recently')
    list_filter = ['publication_date']
    search_fields = ['mpolynomyal', 'structure_name','Mid']
admin.site.register(Mpolynom, MpolynomAdmin)