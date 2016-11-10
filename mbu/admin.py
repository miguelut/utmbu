from django.contrib import admin
from mbu.models import *
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple


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
    form = ScoutAdminForm


@admin.register(ScoutCourseInstance)
class ScoutCourseInstanceAdmin(admin.ModelAdmin):
    filter_horizontal = ('enrollees', )

# Register your models here.

admin.site.register(MeritBadgeUniversity)
admin.site.register(Council)
admin.site.register(Troop)
admin.site.register(Scoutmaster)
admin.site.register(Course)
admin.site.register(TimeBlock)
admin.site.register(ScoutmasterRequest, ScoutmasterRequestAdmin)
admin.site.register(Payment)
admin.site.register(Parent)

