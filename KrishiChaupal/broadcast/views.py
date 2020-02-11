from django.shortcuts import render
from django.conf import settings
from twilio.rest import Client
from django.http import HttpResponse
from .forms import Broadcast
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
@staff_member_required
def broadcast_sms(request):
    form=Broadcast()
    context={}
    if request.method=="POST":
        form=Broadcast(request.POST)
        form.save()
        if form.is_valid():
            print("success")
            message_to_broadcast=form.cleaned_data['alert']
            client= Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
            SMS_BROADCAST_TO_NUMBERS=['+917007110758','+919721882627',]
            for recipient in SMS_BROADCAST_TO_NUMBERS:
                if recipient:
                    client.messages.create(to=recipient,from_=settings.TWILIO_NUMBER,body=message_to_broadcast)
    context.update({'form':form})
    return render(request,"index.html",context=context)
