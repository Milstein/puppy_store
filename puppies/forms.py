from django.forms import forms, ModelForm

from puppies.models import Puppy


class PuppyForm(ModelForm):

    class Meta(object):
        model = Puppy
        fields = ('name', 'age', 'breed', 'color')
