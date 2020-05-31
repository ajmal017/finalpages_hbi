from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from django.contrib.auth.decorators import login_required
from .models import Listing
from members.models import MemberProfile
from django.utils import timezone
from .forms import ListingForm


def listall(request):
  #listings = Listing.objects.order_by('-list_date').filter(is_published=True)
  listings = Listing.objects.all()

  paginator = Paginator(listings, 5)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
  }

  return render(request, 'listings/listings.html', context)

# david007
def listselected(request, listing_id):                 #display individual items
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    'listing': listing
  }

  return render(request, 'listings/listing.html', context)

def search(request):
  queryset_list = Listing.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)

  # State
  if 'state' in request.GET:
    state = request.GET['state']
    if state:
      queryset_list = queryset_list.filter(state__iexact=state)

  # Bedrooms
  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # Price
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'state_choices': state_choices,
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET
  }
  return render(request, 'listings/search.html', context)

#######################################################################################################

@login_required
def upload_brochure(request):
    my_qs = MemberProfile.objects.filter(username=request.user)
    initial_data = {
        'contributor': MemberProfile.objects.get(username=request.user),
        'type': 'BROCHURE',
        'country': my_qs[0].brochure_country,
        'list_date': timezone.now
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ListingForm(initial=initial_data)
        context = {"heading": "Upload Brochure Document",
                    "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)

@login_required
def upload_certificate(request):
    my_qs = MemberProfile.objects.filter(username=request.user)
    initial_data = {
        'contributor': MemberProfile.objects.get(username=request.user),
        'type': 'CERTIFICATE',
        'country': my_qs[0].certificate_country,
        'list_date': timezone.now
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ListingForm(initial=initial_data)
        context = {"heading": "Upload Certificate Document",
                    "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)

@login_required
def upload_eproof(request):
    my_qs = MemberProfile.objects.filter(username=request.user)
    initial_data = {
        'contributor': MemberProfile.objects.get(username=request.user),
        'type': 'E-PROOF',
        'country': my_qs[0].eproof_country,
        'list_date': timezone.now
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ListingForm(initial=initial_data)
        context = {"heading": "Upload Electronic-Proof Document",
                    "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)

@login_required
def upload_manual(request):
    my_qs = MemberProfile.objects.filter(username=request.user)
    initial_data = {
        'contributor': MemberProfile.objects.get(username=request.user),
        'type': 'MANUAL',
        'country': my_qs[0].manual_country,
        'list_date': timezone.now
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ListingForm(initial=initial_data)
        context = {"heading": "Upload Manual Document",
                    "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)

@login_required
def upload_proposal(request):
    my_qs = MemberProfile.objects.filter(username=request.user)
    initial_data = {
        'contributor': MemberProfile.objects.get(username=request.user),
        'type': 'PROPOSAL',
        'country': my_qs[0].proposal_country,
        'list_date': timezone.now
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ListingForm(initial=initial_data)
        context = {"heading": "Upload Proposal Document",
                    "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)

@login_required
def upload_powerpoint(request):
    my_qs = MemberProfile.objects.filter(username=request.user)
    initial_data = {
        'contributor': MemberProfile.objects.get(username=request.user),
        'type': 'POWERPOINT',
        'country': my_qs[0].powerpoint_country,
        'list_date': timezone.now
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ListingForm(initial=initial_data)
        context = {"heading": "Upload PowerPoint Document",
                    "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)


@login_required
def upload_quotation(request):
    my_qs = MemberProfile.objects.filter(username=request.user)
    initial_data = {
        'contributor': MemberProfile.objects.get(username=request.user),
        'type': 'QUOTATION',
        'country': my_qs[0].quotation_country,
        'list_date': timezone.now
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ListingForm(initial=initial_data)
        context = {"heading": "Upload Quotation Document",
                    "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)

@login_required
def alldocuments(request):
    if request.user.is_authenticated:
        qs = Listing.objects.all()
        context = {"title": "All Documents", 'blog_list': qs }
        return render(request, "hbi-dashboard/alldocuments.html", context)

@login_required
def mydocuments(request):
    if request.user.is_authenticated:
        my_qs = MemberProfile.objects.filter(username=request.user)
        qs = Listing.objects.filter(contributor=my_qs[0])
        context = {"title": "My Documents", 'listing': qs}
        return render(request, "hbi-dashboard/mydocuments_old.html", context)

#david007
@login_required
def selecteddocument(request, listing_id):                 #display individual items
  listing = get_object_or_404(Listing, pk=listing_id)
  context = {
    'listing': listing
  }
  return render(request, 'hbi-dashboard/selecteddocument.html', context)
