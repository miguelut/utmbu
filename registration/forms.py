from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from scout.models import Scout


ScoutFormSet = inlineformset_factory(User, Scout, can_delete=False)
