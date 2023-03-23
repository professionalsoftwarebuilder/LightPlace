from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import ContactForm

#from core.models import CardSession



def contact(request):
    form_class = ContactForm

    return render(request, 'contact/contact.html', {
        'form': form_class,
    })

