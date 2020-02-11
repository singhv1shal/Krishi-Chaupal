from django.views.generic import TemplateView

class suggest(TemplateView):
    template_name="advisory.html"
class weather(TemplateView):
    template_name="weather.html"
