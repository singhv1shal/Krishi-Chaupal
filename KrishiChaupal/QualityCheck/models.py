from django.db import models

class PestCheck(models.Model):
    Uploaded_image=models.ImageField(upload_to='Leaves')
    crop_name=models.CharField(max_length=254)
