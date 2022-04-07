from django import forms


class SubmitForm(forms.Form):
    title = forms.CharField(label='title', max_length=100)
    url = forms.CharField(label='url', max_length=100)
    text = forms.CharField(label='text', max_length=1000)