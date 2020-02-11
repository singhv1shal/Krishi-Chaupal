from django.conf.urls import url
from . import views

app_name='broadcast'

urlpatterns=[
    url(r'^$',views.broadcast_sms,name="broadcast_sms"),
]
