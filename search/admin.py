from django.contrib import admin
from .models import Mpolynom
from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.contrib.admin import helpers
from django.contrib.admin.options import csrf_protect_m, IS_POPUP_VAR
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str

from django.forms.forms import NON_FIELD_ERRORS
from django.db.models import Q
from simple_history.admin import SimpleHistoryAdmin


class MpolynomAdminForm(forms.ModelForm):
    class Meta:
            model = Mpolynom
            fields = ('mpolynomial_see', 'structure_name', 'keywords', 
                'new_keywords', 'comments', 'new_comments', 'references', 
                'new_references','links', 'new_links','status', 
                'new_comments_authors')
    
    def clean(self):
        # check inputed mpoly before saving
        input_string = self.cleaned_data.get('mpolynomial_see')
        if not input_string:
            raise ValidationError('')
        if input_string[len(input_string)-1] == "^" or input_string[0] == "^":
            raise ValidationError('''M-polynomial variable or variable power 
                missing''')
        if input_string[len(input_string)-1] == "+":
            raise ValidationError('M-polynomial ends with + sign')
        if input_string[len(input_string)-1] == "-":
            raise ValidationError('M-polynomial ends with - sign')
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
            raise ValidationError('''Parentheses do not match. Please correct 
                the M-polynomial.''')
        return self.cleaned_data


class CommentAdminForm(forms.ModelForm):
    class Meta:
            model = Mpolynom
            fields = ('new_keywords', 'new_comments', 'new_references',
                'new_links')

    # change initial value
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['new_keywords'] = ''
        initial['new_comments'] = ''
        initial['new_references'] = ''
        initial['new_links'] = ''
        kwargs['initial'] = initial
        super(CommentAdminForm, self).__init__(*args, **kwargs)
     

class MpolynomModelAdmin(admin.ModelAdmin):
    form = MpolynomAdminForm

    def save_model(self, request, obj, form, change):
        results = Mpolynom.objects.filter(Mid = obj.Mid).values()
        if results:
            if obj.status == "approved":
                kw = obj.new_keywords + " ," + obj.keywords
                obj.keywords = kw.strip(" ,")
                obj.new_keywords = ""

                com = obj.new_comments + " ," + obj.comments
                obj.comments = com.strip(" ,")
                obj.new_comments = ""

                ref = obj.new_references + " ," + obj.references
                obj.references = ref.strip(" ,")
                obj.new_references = ""

                lin = obj.new_links + " ," + obj.links
                obj.links = lin.strip(" ,")
                obj.new_links = ""

                obj.new_comments_authors = ""

        if change == True:
                obj.author = obj.author
                obj.author_username = obj.author_username
        else:
            obj.author_username = request.user.username
            if request.user.first_name and request.user.last_name:
                obj.author = (request.user.first_name + " " + 
                request.user.last_name)
            else:
                obj.author = request.user.username
        obj.save()

    # makes database and parentheses errors displayed on admin page when 
    # adding M-polynomial
    def add_view(self, request, form_url='', extra_context=None):
        try:
            return super(MpolynomModelAdmin, self).add_view(request, form_url, 
                extra_context)
        except (IntegrityError, DatabaseError) as e:
            if (str(e) == 
                'UNIQUE constraint failed: search_mpolynom.structure_name'):
                e = '''Structure name already exists! Check if the M-polynomial
                    already exists in the database.'''
            model = self.model
            opts = model._meta
            formsets = []
            inline_instances = self.get_inline_instances(request, None)
            form = MpolynomAdminForm(request.POST, request.FILES)
            form.is_valid()
            # make faked nonfield error
            form._errors[NON_FIELD_ERRORS] = form.error_class([e])
            # We may handle exception here (just to save indentation)
            adminForm = helpers.AdminForm(form, 
                list(self.get_fieldsets(request)),
                self.get_prepopulated_fields(request),
                self.get_readonly_fields(request),
                model_admin=self)
            media = self.media + adminForm.media

            inline_admin_formsets = []
            for inline, formset in zip(inline_instances, formsets):
                fieldsets = list(inline.get_fieldsets(request))
                readonly = list(inline.get_readonly_fields(request))
                prepopulated = dict(inline.get_prepopulated_fields(request))
                inline_admin_formset = helpers.InlineAdminFormSet(inline, 
                    formset,fieldsets, prepopulated, readonly, 
                    model_admin=self)
                inline_admin_formsets.append(inline_admin_formset)
                media = media + inline_admin_formset.media
            context = {
                'title': _('Add %s') % force_str(opts.verbose_name),
                'adminform': adminForm,
                'is_popup': IS_POPUP_VAR in request,
                'media': media,
                'inline_admin_formsets': inline_admin_formsets,
                'errors': helpers.AdminErrorList(form, formsets),
                'app_label': opts.app_label,
                'preserved_filters': self.get_preserved_filters(request),
                
            }
            context.update(extra_context or {})
            return self.render_change_form(request, context, form_url=form_url, 
                add=True)

    # makes database and parentheses errors displayed on admin page when 
    # changing M-polynomial
    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            # get the default template response
            template_response = super(MpolynomModelAdmin, self).change_view(
                request, object_id, form_url, extra_context)
            # hide buttons
            if not request.user.is_superuser:
                if object_id:
                    obj = Mpolynom.objects.get(pk=object_id)
                    if obj:
                        if (obj.status == 'new_comments' or 
                            obj.status == 'approved'):
                            # hide the div that contains the save and 
                            # delete buttons
                            template_response.content = (
                                template_response.rendered_content.replace(
                                '<div class="submit-row">',
                                '<div class="submit-row" style="display: none">'
                                ))
            return template_response
        except (IntegrityError, DatabaseError) as e:
            if (str(e) == 
                'UNIQUE constraint failed: search_mpolynom.structure_name'):
                e = '''Structure name already exists! Check if the M-polynomial 
                    already exists in the database.'''
            model = self.model
            opts = model._meta
            formsets = []
            inline_instances = self.get_inline_instances(request, None)
            form = MpolynomAdminForm(request.POST, request.FILES)
            form.is_valid()
            # make faked nonfield error
            form._errors[NON_FIELD_ERRORS] = form.error_class([e])
            # We may handle exception here (just to save indentation)
            adminForm = helpers.AdminForm(form, list(
                self.get_fieldsets(request)),
                self.get_prepopulated_fields(request),
                self.get_readonly_fields(request),
                model_admin=self)
            media = self.media + adminForm.media

            inline_admin_formsets = []
            for inline, formset in zip(inline_instances, formsets):
                fieldsets = list(inline.get_fieldsets(request))
                readonly = list(inline.get_readonly_fields(request))
                prepopulated = dict(inline.get_prepopulated_fields(request))
                inline_admin_formset = helpers.InlineAdminFormSet(inline, 
                    formset, fieldsets, prepopulated, readonly, 
                    model_admin=self)
                inline_admin_formsets.append(inline_admin_formset)
                media = media + inline_admin_formset.media
            context = {
                'title': _('Add %s') % force_str(opts.verbose_name),
                'adminform': adminForm,
                'is_popup': IS_POPUP_VAR in request,
                'media': media,
                'inline_admin_formsets': inline_admin_formsets,
                'errors': helpers.AdminErrorList(form, formsets),
                'app_label': opts.app_label,
                'preserved_filters': self.get_preserved_filters(request),
            }
            context.update(extra_context or {})
            return self.render_change_form(request, context, form_url=form_url, 
                add=True)
           
    #non-superuser users can see only their inputs
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author_username = request.user.username)

    # if user has more than 50 unresolved(status waiting) objects cant add new
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            by_author = Mpolynom.objects.filter(
                author_username=request.user.username)
            by_author_waiting = by_author.filter(status="waiting")
            nb_author_waiting = by_author_waiting.count()
            if nb_author_waiting > 50:
                return False
            else:
                return True

    # hide save buttons for objects with approval or new_comments status for 
    # non superusers
    def changeform_view(self, request, object_id=None, form_url='', 
        extra_context=None):
        extra_context = extra_context or {}
        if not request.user.is_superuser:
            if object_id:
                obj = Mpolynom.objects.get(pk=object_id)
                if obj:
                    if obj.status == 'new_comments' or obj.status == 'approved':
                        extra_context['show_save'] = False
                        extra_context['show_save_and_continue'] = False
                        extra_context['show_save_and_add_another'] = False
        try:
            return super().changeform_view(request, object_id, 
                extra_context=extra_context)
        except IOError as err:
            self.message_user(request, str(err), level=messages.ERROR)
            return HttpResponseRedirect(request.path)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                if obj.status == "new_comments" or obj.status == 'approved':
                    return self.readonly_fields + ('mpolynomial_see', 
                        'structure_name', 'Mid', 'author','published_recently', 
                        'status', 'keywords', 'comments', 'references', 
                        'links', 'new_keywords', 'new_comments', 
                        'new_references', 'new_links', 'new_comments_authors')
            return self.readonly_fields + ('status','new_keywords', 
                'new_comments', 'new_references', 'new_links', 
                'new_comments_authors')
        return self.readonly_fields + ('new_comments_authors',)

    list_display = ('mpolynomial_see', 'structure_name', 'Mid', 'author', 
        'author_username','published_recently', 'status',)
    list_filter = ['publication_date']
    search_fields = ['mpolynomial_see', 'structure_name','author',
        'author_username','Mid', 'status']

admin.site.register(Mpolynom, MpolynomModelAdmin)


class Comment(Mpolynom):
    # class Mpolynom can be registered only once, create fake class Comment 
    # wich is basically Mpolynom class
    class Meta:
        proxy = True


class CommentAdmin(SimpleHistoryAdmin):
    form = CommentAdminForm

    def save_model(self, request, obj, form, change):
        obj.status = "new_comments"
        results = Mpolynom.objects.filter(Mid = obj.Mid).values()
        new_keywords = results[0].get("new_keywords")
        new_comments = results[0].get("new_comments")
        new_references = results[0].get("new_references")
        new_links = results[0].get("new_links")
        new_comments_authors = results[0].get("new_comments_authors")

        if obj.new_keywords:
            kw = obj.new_keywords + ", " + new_keywords
            obj.new_keywords = kw.strip(" ,")

        if obj.new_comments:
            com = obj.new_comments + ", " + new_comments
            obj.new_comments = com.strip(" ,")

        if obj.new_references:
            ref = obj.new_references + ", " + new_references
            obj.new_references = ref.strip(" ,")

        if obj.new_links:
            lin = obj.new_links + ", " + new_links
            obj.new_links = lin.strip(" ,")

        if (obj.new_keywords or obj.new_comments or obj.new_references 
            or obj.new_links):
            nc_author = request.user.username
            if nc_author in new_comments_authors:
                ca = new_comments_authors
            else:
                ca = nc_author + ", " + new_comments_authors
            obj.new_comments_authors = ca.strip(" ,")
        obj.save()

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            new_comments = Mpolynom.objects.filter(
                new_comments_authors__contains=request.user.username)
            nb_new_comments = new_comments.count()
            if nb_new_comments > 50:
                return False
            else:
                return True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        can_change = qs.filter(Q(status="approved") | Q(status="new_comments"))
        return can_change

    list_display = ('mpolynomial_see', 'structure_name', 'Mid', 'author', 
        'author_username','published_recently', 'status')
    list_filter = ['publication_date']
    search_fields = ['mpolynomial_see', 'structure_name','author', 
        'author_username','Mid','status']
    history_list_display = ['Mid','new_keywords', 'new_comments',
        'new_references','new_links']

admin.site.register(Comment, CommentAdmin)

