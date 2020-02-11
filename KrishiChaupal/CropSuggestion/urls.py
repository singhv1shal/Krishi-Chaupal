from django.conf.urls import url
from . import views

app_name='CropSuggestion'

urlpatterns=[
    url(r'^$',views.suggest.as_view(),name="suggest"),
    url(r'weather/',views.weather.as_view(),name="weather"),
]
