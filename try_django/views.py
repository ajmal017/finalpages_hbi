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
from members.models import MemberProfile
from django.views.generic import View
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost
from listings.models import Listing
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from datetime import datetime
from documents.models import ProposalModel, ProductModel, RawProductModel
from documents.forms import ProposalForm, ProductForm, RawProductForm
from listings.forms import ListingForm
from django.utils import timezone

def upload3(request):
    my_form = RawProductForm()
    if request.method == 'POST':
        my_form = RawProductForm(request.POST)
        if my_form.is_valid():
            print(my_form.cleaned_data)
            RawProductModel.objects.create(**my_form.cleaned_data)
        return render(request, "hbi-dashboard/dashboard.html")
    context = {
        'form': my_form,
        'title': 'upload3'
        }
    return render(request, "hbi-dashboard/upload3.html", context)


def upload4(request):
    initial_data = {
        'title': 'This is my awesome title'
    }
    # for modifying database elements thru the use of forms - add below 2 steps
    #obj = ProductModel.objects.get(id=1) #for grabbing an existing data element for modifications
    #form = ProductForm(request.POST or None, instance=obj)

    form = ProductForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        form.save()
        form = ProductForm()
        return render(request, "hbi-dashboard/dashboard.html")
    context = {
        'title': 'upload4.html',
        'form': form}
    return render(request, "hbi-dashboard/upload4.html", context)

# combine upload1 and upload4
def upload5(request):
    my_qs = MemberProfile.objects.get(username=request.user)
    print ('110. username      =',my_qs.username)
    print ('111. user firstname=', my_qs.first_name)
    initial_data = {
        'contributor': MemberProfile.objects.get(username=request.user),
        'type': 'BROCHURE',
        'country': 'CAMBODIA',
        'description': 'ABCDEF',
        'list_date': timezone.now
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ListingForm(initial=initial_data)
    return render(request, 'hbi-dashboard/upload5.html', {
        'form': form
    })

#working ok
def upload1(request):
    if request.method == 'POST':
        form = ProposalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProposalForm()
    return render(request, 'hbi-dashboard/upload1.html', {
        'form': form
    })

#does not work!
def upload2(request):
    if request.method == 'POST':
        my_qs = MemberProfile.objects.filter(username=request.user)
        title = request.POST.get('title')
        description = request.POST.get('description')
        pdf = request.POST.get('pdf')
        cover = request.POST.get('cover')
        print('10. title =', title)
        print('20. author =', my_qs[0].username)
        print('30. description =', description)
        print('40. pdf=', pdf)
        print('50. cover=', cover)
        newdoc = ProposalModel()
        newdoc.title = title
        newdoc.author = my_qs[0]
        newdoc.description = description
        current_day = datetime.now().strftime('%d')
        current_month = datetime.now().strftime('%m')
        current_year = datetime.now().strftime('%Y')
        newdoc.pdf = "proposals/pdfs/" + str(current_year) + '/' + str(current_month) + '/' + str(current_day) + '/' + str(pdf)
        newdoc.cover = "proposals/covers/" + str(current_year) + '/' + str(current_month) + '/' + str(current_day) + '/' + str(cover)
        #newdoc.pdf = pdf
        #newdoc.cover = cover
        newdoc.save()
        return redirect('dashboard')
    else:
        my_qs = MemberProfile.objects.filter(username=request.user)
        print('1. firstname=', my_qs[0].first_name)
        context = {"title": "mysettings.html", 'blog_list': my_qs[0]}
        return render(request, 'hbi-dashboard/upload2.html', context)





@login_required
def blank(request):
    if request.user.is_authenticated:
        qs = BlogPost.objects.all()
        context = {"title": "blank.html", 'blog_list': qs}
        return render(request, "hbi-dashboard/blank.html", context)



def forecast(request):
    qs = Listing.objects.all()
    context = {"title": "testcard.html", 'blog_list': qs}
    return render(request, "hbi-dashboard/cards.html", context)


def signup(request):
    qs = BlogPost.objects.all()
    context = {"title": "signup.html", 'blog_list': qs}
    return render(request, "signup/signup.html", context)

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        context = {"title": "dashboard.html", 'blog_list': my_qs}
        return render(request, "hbi-dashboard/dashboard.html", context)



def okr(request):
    qs = BlogPost.objects.all()
    context = {"title": "index.html", 'blog_list': qs}
    return render(request, "hbi-dashboard/new-blank.html", context)



def po(request):
    qs = BlogPost.objects.all()
    context = {"title": "index.html", 'blog_list': qs}
    return render(request, "conceptmaster/index.html", context)


def demo(request):
    qs = BlogPost.objects.all()
    context = {"title": "index.html", 'blog_list': qs}
    return render(request, "demo/index.html", context)

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




def index(request):
    if request.user.is_authenticated:
        my_qs = MemberProfile.objects.filter(username=request.user)
        context = {"title": "index.html", 'blog_list': my_qs}
        return render(request, 'hbi-dashboard/dashboard.html', context)
    else:
        qs = Listing.objects.all()
        context = {"title": "index.html", 'blog_list': qs}
        return render(request, "hbi-homepage/index.html", context)

