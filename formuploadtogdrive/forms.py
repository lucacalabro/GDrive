from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('field1', 'field2', 'document',)
        # fields = "__all__" Non includo tutti i campi in quanto
        # il campo 'uploaded_at' è autogenerato
