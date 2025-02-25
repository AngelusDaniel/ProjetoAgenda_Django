from contact import models
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

@login_required(login_url="contact:login")
def index(request):
    contacts = models.Contact.objects.all()\
    .filter(show=True)\
    .order_by("-id")\
    
    paginator = Paginator(contacts, 10)  # Show 15 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    

    context = {
        'page_obj': page_obj,
        'site_title': f"Contatos - ",
    }

    return render(
        request,
        "contact/index.html",
        context
    )
    
@login_required(login_url="contact:login")
def search(request):
    search_value = request.GET.get("q", "").strip()
    
    if not search_value:
        return redirect("contact:index")


    contacts = models.Contact.objects\
    .filter(show=True)\
    .filter(
        Q(id__icontains=search_value) |
        Q(first_name__icontains=search_value) | 
        Q(last_name__icontains=search_value) |
        Q(phone__icontains=search_value) |
        Q(email__icontains=search_value) 
    )\
    .order_by("-id")\

    paginator = Paginator(contacts, 10)  # Show 15 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'site_title': f"Contatos - ",
        "search_value": search_value,
    }

    return render(
        request,
        "contact/index.html",
        context
    )



def contact(request, contact_id):
    # single_contact = models.Contact.objects.filter(pk=contact_id).first()
    single_contact = get_object_or_404(models.Contact, pk=contact_id,)
    
    contact_name = f"{single_contact.first_name} {single_contact.last_name} - "

    context = {
        'contact': single_contact,
        'site_title': contact_name,
    }

    return render(
        request,
        "contact/contact.html",
        context
    )
