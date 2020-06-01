from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from django.contrib.auth.decorators import login_required
from .models import Listing
from members.models import MemberProfile
from django.utils import timezone
from .forms import ListingForm, EditListingForm


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
        return render(request, "hbi-dashboard/mydocuments.html", context)

@login_required
def selecteddocument(request, listing_id):                 #display individual items
  listing = get_object_or_404(Listing, pk=listing_id)
  context = {
    'listing': listing
  }
  return render(request, 'hbi-dashboard/selecteddocument.html', context)

@login_required
def delete_document(request, listing_id):
    selected_document = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        print('Here at delete document')
        selected_document.delete()
        return render(request, "hbi-dashboard/dashboard.html")

    context = {'item': selected_document,
               'title': 'Delete Document',
              }
    return render(request, 'hbi-dashboard/delete_document.html', context)

def edit_document(request, listing_id):
    selected_customer = get_object_or_404(Listing, pk=listing_id)
    form = EditListingForm(instance=selected_customer)

    if request.method == 'POST':
        form = EditListingForm(request.POST, request.FILES, instance=selected_customer)
        if form.is_valid():
            print('1. form name=', form.cleaned_data['name'])
            #print('2. form salesrep=', form.cleaned_data['salesrep'])
            print('3. form country=', form.cleaned_data['country'])
            print('4. form agent=', form.cleaned_data['agent'])
            form.save()
            return render(request, "hbi-dashboard/dashboard.html")
        else:
            return render(request, "hbi-dashboard/dashboard.html")
    context = {'form':form,
               'title': 'Edit Customer Profile',
               'customer': selected_customer
              }
    return render(request, 'hbi-dashboard/edit_customer.html', context)


#######################################################################################################

@login_required
def upload_brochure(request):
    my_qs = MemberProfile.objects.filter(username=request.user)
    # print ('my_qs.powerpoint_country=',my_qs[0].powerpoint_country)
    initial_data = {
        'country': my_qs[0].brochure_country,
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'])
            # print('1. object title=', selected_item.title)
            my_qs = MemberProfile.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a MemberProfile object into selected_customer.salesrep
            selected_item.type = 'BROCHURE'
            selected_item.save()

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
    # print ('my_qs.powerpoint_country=',my_qs[0].powerpoint_country)
    initial_data = {
        'country': my_qs[0].certificate_country,
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'])
            # print('1. object title=', selected_item.title)
            my_qs = MemberProfile.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a MemberProfile object into selected_customer.salesrep
            selected_item.type = 'CERTIFICATE'
            selected_item.save()

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
    # print ('my_qs.powerpoint_country=',my_qs[0].powerpoint_country)
    initial_data = {
        'country': my_qs[0].eproof_country,
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'])
            # print('1. object title=', selected_item.title)
            my_qs = MemberProfile.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a MemberProfile object into selected_customer.salesrep
            selected_item.type = 'EPROOF'
            selected_item.save()

            return redirect('dashboard')
    else:
        form = ListingForm(initial=initial_data)
        context = {"heading": "Upload E-Proof Document",
                   "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)


@login_required
def upload_manual(request):
    my_qs = MemberProfile.objects.filter(username=request.user)
    # print ('my_qs.powerpoint_country=',my_qs[0].powerpoint_country)
    initial_data = {
        'country': my_qs[0].manual_country,
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'])
            # print('1. object title=', selected_item.title)
            my_qs = MemberProfile.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a MemberProfile object into selected_customer.salesrep
            selected_item.type = 'MANUAL'
            selected_item.save()

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
    # print ('my_qs.powerpoint_country=',my_qs[0].powerpoint_country)
    initial_data = {
        'country': my_qs[0].proposal_country,
    }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'])
            # print('1. object title=', selected_item.title)
            my_qs = MemberProfile.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a MemberProfile object into selected_customer.salesrep
            selected_item.type = 'PROPOSAL'
            selected_item.save()

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
    #print ('my_qs.powerpoint_country=',my_qs[0].powerpoint_country)
    initial_data = {
        'country': my_qs[0].powerpoint_country,
        }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'])
            #print('1. object title=', selected_item.title)
            my_qs = MemberProfile.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a MemberProfile object into selected_customer.salesrep
            selected_item.type = 'POWERPOINT'
            selected_item.save()

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
    #print ('my_qs.powerpoint_country=',my_qs[0].powerpoint_country)
    initial_data = {
        'country': my_qs[0].quotation_country,
        }
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'])
            #print('1. object title=', selected_item.title)
            my_qs = MemberProfile.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a MemberProfile object into selected_customer.salesrep
            selected_item.type = 'QUOTATION'
            selected_item.save()

            return redirect('dashboard')
    else:
        form = ListingForm(initial=initial_data)
        context = {"heading": "Upload Quotation Document",
                    "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)



#######################################################################################################

