from django.contrib import admin
from .models import Mpolynom
from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect


# Register your models here.
# diplay mpolynom on the admin page
#admin.site.unregister(Mpolynom)

class MpolynomAdminForm(forms.ModelForm):
    def clean(self):
        input_string = self.cleaned_data.get('mpolynomyal')
        s = []
        balanced = True
        index = 0
        while index < len(input_string) and balanced:
            token = input_string[index]
            if token == "(":
                s.append(token)
            elif token == ")":
                if len(s) == 0:
                    balanced = False
                else:
                    s.pop()
            index += 1
        val = balanced and len(s) == 0
        if not val:
            raise ValidationError('Parentheses do not match. Please correct M-polynoial.')
        return self.cleaned_data


class MpolynomAdmin(admin.ModelAdmin):
    form = MpolynomAdminForm

    # non-superuser users can change only their inputs
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    def save_model(self, request, obj, form, change):
        obj.author = request.user.username
        obj.save()

    def changeform_view(self, request, *args, **kwargs):
        try:
            return super().changeform_view(request, *args, **kwargs)
        except IOError as err:
            self.message_user(request, str(err), level=messages.ERROR)
            return HttpResponseRedirect(request.path)


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