from contact import models
from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Create your views here.

def index(request):
    contacts = models.Contact.objects.all()\
    .filter(show=True)\
    .order_by("-id")[0:10]\
    
    print(contacts.query)
    context = {
        'contacts': contacts,
    }

    return render(
        request,
        "contact/index.html",
        context
    )

def contact(request, contact_id):
    # single_contact = models.Contact.objects.filter(pk=contact_id).first()
    single_contact = get_object_or_404(models.Contact, pk=contact_id,)
    
    print(single_contact)
    context = {
        'contact': single_contact,
    }

    return render(
        request,
        "contact/contact.html",
        context
    )
