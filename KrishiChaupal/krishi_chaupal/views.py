from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

class TestPage(TemplateView):
    template_name='test.html'

class ThanksPage(TemplateView):
    template_name='thanks.html'

class HomePage(TemplateView):
    template_name="home.html"

class AboutPage(TemplateView):
    template_name="about.html"

class faq(TemplateView):
    template_name="faq.html"

class rice(TemplateView):
    template_name="rice.html"

class wheat(TemplateView):
    template_name="wheat.html"

class risks(TemplateView):
    template_name="risks.html"

class sugarcane(TemplateView):
    template_name="sugarcane.html"

class readmore(TemplateView):
    template_name="readmore.html"

def maize(request):
    return HttpResponse("We are still working on that")
