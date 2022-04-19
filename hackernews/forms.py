from dataclasses import field
from django import forms
from matplotlib import widgets
from .models import User
from django.forms import ModelForm

class UserForm(ModelForm):
    showdead = forms.ChoiceField(choices=(("True","yes"),("False", "no")))
    noprocrast = forms.ChoiceField(choices=(("True","yes"),("False", "no")))
    
    class Meta:
        model = User
        fields = ('about', 'email', 'showdead', 'noprocrast', 'maxvisit', 'minaway', 'delay')
        widgets = {
            'about' : forms.Textarea(attrs={'cols':"60", 'rows':"5", 'wrap':"virtual"}),
            'email' : forms.EmailInput(attrs={'size':"60"}),
            'maxvisit' : forms.TextInput(attrs={'size':'16'}),
            'minaway' : forms.TextInput(attrs={'size':'16'}),
            'delay' : forms.TextInput(attrs={'size':'16'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(UserForm, self).save()

class SubmitForm(forms.Form):
    title = forms.CharField(label='title', max_length=100)
    url = forms.CharField(label='url', max_length=100)
    text = forms.CharField(label='text', max_length=1000)
