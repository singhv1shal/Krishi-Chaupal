from django.forms import ModelForm
from .models import PestCheck

class UploadImage(ModelForm):
    class Meta:
        model=PestCheck
        fields=('crop_name','Uploaded_image')
