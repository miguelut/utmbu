from django.forms import ModelForm
from scout.models import Scout

class ScoutForm(ModelForm):
    class Meta:
        model = Scout
        fields = ['User.first_name']
