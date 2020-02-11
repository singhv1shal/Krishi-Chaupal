"""krishi_chaupal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.HomePage.as_view(),name='home'),
    url(r'^about/',views.AboutPage.as_view(),name='about'),
    url(r'^faq/',views.faq.as_view(),name='faq'),
    url(r'^rice/',views.rice.as_view(),name='rice'),
    url(r'^wheat/',views.wheat.as_view(),name='wheat'),
    url(r'^sugarcane/',views.sugarcane.as_view(),name='sugarcane'),
    url(r'^risks/',views.risks.as_view(),name='risks'),
    url(r'^maize/',views.maize,name='maize'),
    url(r'^readmore/',views.readmore.as_view(),name='readmore'),
    url(r'accounts/',include('accounts.urls',namespace='accounts')),
    # url(r'chatbot/',include('chatbot.urls',namespace='chatbot')),
    url(r'broadcast/',include('broadcast.urls',namespace='broadcast')),
    url(r'loans/',include('loans.urls',namespace='loans')),
    url(r'QualityCheck/',include('QualityCheck.urls',namespace='QualityCheck')),
    url(r'CropSuggestion/',include('CropSuggestion.urls',namespace='CropSuggestion')),
    url(r'accounts/',include('django.contrib.auth.urls')),
    url(r'^test/$',views.TestPage.as_view(),name='test'),
    url(r'^thanks/$',views.ThanksPage.as_view(),name='thanks')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
