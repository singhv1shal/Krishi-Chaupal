from django.conf.urls import url
from . import views

app_name='QualityCheck'

urlpatterns=[
    url(r'^$',views.UploadImage_view,name='UploadImage_view'),

]
