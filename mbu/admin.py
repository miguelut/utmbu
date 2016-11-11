from mbu.models import *
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple


@admin.register(Council)
class CouncilAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'city', 'state')
    search_fields = ('name', 'city', 'state')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_first_name', 'user_last_name', 'amount', 'status')
    search_fields = ('user__first_name', 'user__last_name', 'status')

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = "First Name"

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = "Last Name"


class ScoutAdminForm(forms.ModelForm):
    enrollments = forms.ModelMultipleChoiceField(
        queryset=ScoutCourseInstance.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Enrollments'),
            is_stacked=False
        )
    )

    class Meta:
        model = Scout
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ScoutAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['enrollments'].initial = self.instance.enrollments.all()

    def save(self, commit=True):
        scout = super(ScoutAdminForm, self).save(commit=False)

        if commit:
            scout.save()

        if scout.pk:
            scout.enrollments = self.cleaned_data['enrollments']
            self.save_m2m()

        return scout


@admin.register(Scout)
class ScoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_first_name', 'user_last_name', 'user_email', 'troop')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    form = ScoutAdminForm

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = "First Name"

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = "Last Name"

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "Email Address"


@admin.register(ScoutCourseInstance)
class ScoutCourseInstanceAdmin(admin.ModelAdmin):
    filter_horizontal = ('enrollees', )


@admin.register(Troop)
class TroopAdmin(admin.ModelAdmin):
    list_display = ('number', 'council')
    search_fields = ('number',)

# Register your models here.

admin.site.register(MeritBadgeUniversity)
admin.site.register(Scoutmaster)
admin.site.register(Course)
admin.site.register(TimeBlock)
admin.site.register(ScoutmasterRequest, ScoutmasterRequestAdmin)
admin.site.register(Parent)

