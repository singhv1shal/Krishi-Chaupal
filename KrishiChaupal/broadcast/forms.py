from django import forms
from .models import messages
class Broadcast(forms.ModelForm):
    class Meta:
        model=messages
        fields=('alert',)
        widget={
        'name': forms.Textarea(attrs={'placeholder':'Broadcast your message' ,'id':'text','rows':'4' ,'style':'overflow: hidden; word-wrap: break-word; resize: none; height: 160px;'})
        }
