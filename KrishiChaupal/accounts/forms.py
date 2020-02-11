from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Userdetail

class UserCreateForm(UserCreationForm):
    phone_number=forms.CharField(required=True)
    location=forms.CharField(required=True)
    class Meta:
        model = Userdetail
        fields = ("username", "phone_number","location", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=True)
        user.phone_number = self.cleaned_data["phone_number"]
        user.location=self.cleaned_data["location"]
        if commit:
            user.save()
        return user
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #assigning label for actual field
        self.fields['username'].label='Username'
