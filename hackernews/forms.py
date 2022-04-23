from dataclasses import field
from django import forms
from .models import User
from django.forms import ModelForm

class UserForm(ModelForm):
    showdead = forms.ChoiceField(choices=(("True","yes"),("False", "no")))
    noprocrast = forms.ChoiceField(choices=(("True","yes"),("False", "no")))
    
    class Meta:
        model = User
        fields = ('about','showdead', 'noprocrast', 'maxvisit', 'minaway', 'delay')
        widgets = {
            'about' : forms.Textarea(attrs={'cols':"60", 'rows':"5", 'wrap':"virtual"}),
            'maxvisit' : forms.TextInput(attrs={'size':'16'}),
            'minaway' : forms.TextInput(attrs={'size':'16'}),
            'delay' : forms.TextInput(attrs={'size':'16'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(UserForm, self).save()
