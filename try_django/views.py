from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from members.models import account_activation_token
from members.models import Member
from django.views.generic import View
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from datetime import datetime

from listings.forms import ListingForm
from django.utils import timezone

@login_required
def blank(request):
    if request.user.is_authenticated:
        context = {"title": "BLANK"}
        return render(request, "hbi-dashboard/blank.html", context)



def forecast(request):
    qs = Listing.objects.all()
    context = {"title": "testcard.html", 'blog_list': qs}
    return render(request, "hbi-dashboard/cards.html", context)



@login_required
def dashboard(request):
    if request.user.is_authenticated:
        context = {"title": "My Dashboard"}
        return render(request, "hbi-dashboard/dashboard.html", context)

@login_required
def gallery(request):
    if request.user.is_authenticated:
        context = {"title": "Cards Gallery"}
        return render(request, "hbi-dashboard/gallery.html", context)


def about_page(request):
    return render(request, "about.html", {"title": "About"})


def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {
        "title": "Contact us", 
        "form": form
    }
    return render(request, "form.html", context)

def gallery(request):
    context = {"title": "Hengbao Cards Gallery"}
    return render(request, 'hbi-homepage/gallery.html', context)


def index(request):
    if request.user.is_authenticated:
        my_qs = Member.objects.filter(username=request.user)
        context = {"title": "index.html", 'blog_list': my_qs}
        return render(request, 'hbi-dashboard/dashboard.html', context)
    else:
        qs = Listing.objects.all()
        context = {"title": "index.html", 'blog_list': qs}
        return render(request, "hbi-homepage/index.html", context)

