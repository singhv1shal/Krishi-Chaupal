from django.conf.urls import url
from . import views

app_name='loans'

urlpatterns=[
    url(r'canara/$',views.canara.as_view(),name="canara"),
    url(r'cbi/',views.cbi,name="cbi"),
    url(r'bom/',views.loan.as_view(),name="bom"),
    url(r'cb/',views.loan.as_view(),name="cb"),
    url(r'iob/',views.iob,name="iob"),
    url(r'uco/',views.loan.as_view(),name="uco"),
    url(r'bb/',views.loan.as_view(),name="bb"),
]
