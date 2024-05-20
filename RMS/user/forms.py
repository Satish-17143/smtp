from django import forms
from .models import smtp

class RequestForm(forms.ModelForm):
    class Meta:
        model = smtp
        fields = ['Name', 'Phone', 'Email', 'Location', 'Message']
    