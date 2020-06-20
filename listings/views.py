from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from django.contrib.auth.decorators import login_required
from .models import Listing, Eproof
from members.models import Member
from .forms import ListingForm, EproofForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ListingSerializer

@api_view(['GET'])
def mydocumentsOverview(request):
    api_urls = {
        'List':'/task-list/',
        'Detail View':'/task-detail/<str:pk>/',
        'Create':'/task-create/',
        'Update':'/task-update/<str:pk>/',
        'Delete':'/task-delete/<str:pk>/',
        }
    return Response(api_urls)

@api_view(['GET'])
def mydocumentstaskList(request):
    tasks = Listing.objects.all().order_by('-id')
    serializer = ListingSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def mydocumentstaskDetail(request, pk):
    tasks = Listing.objects.get(id=pk)
    serializer = ListingSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def mydocumentstaskCreate(request):
    serializer = ListingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def mydocumentstaskUpdate(request, pk):
    task = Listing.objects.get(id=pk)
    serializer = ListingSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        print('Serializer is valid')
        serializer.save()
    else:
        print('Serializer is NOT valid')
    return Response(serializer.data)

@api_view(['DELETE'])
def mydocumentstaskDelete(request, pk):
    task = Listing.objects.get(id=pk)
    task.delete()
    return Response('Item succsesfully delete!')








##########################################################################

@login_required
def mydocumentslist(request):
    if request.user.is_authenticated:
        my_qs = Member.objects.filter(username=request.user)
        qs = Listing.objects.filter(contributor=my_qs[0])
        context = {"title": "HBI List.html", 'my_qs': my_qs}
        return render(request, "hbi-dashboard/list.html", context)



@login_required
def change_ispublished(request, items):
    # for item_id
    #selected_document = get_object_or_404(Listing, pk=listing_id)
    pass

@login_required
def alldocuments(request):
    if request.user.is_authenticated:
        qs = Listing.objects.all()
        context = {"title": "All Documents", 'blog_list': qs }
        return render(request, "hbi-dashboard/alldocuments.html", context)

@login_required
def mydocuments(request):
    if request.user.is_authenticated:
        my_qs = Member.objects.filter(username=request.user)
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
        print('Here at delete document 123')
        selected_document.delete()
        return render(request, "hbi-dashboard/dashboard.html")

    context = {'item': selected_document,
               'title': 'Delete Document',
              }
    return render(request, 'hbi-dashboard/delete_document.html', context)

def edit_document(request, listing_id):
    selected_document = get_object_or_404(Listing, pk=listing_id)
    form = ListingForm(instance=selected_document)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=selected_document)
        if form.is_valid():
            print('1. form title=', form.cleaned_data['title'])
            print('2. form description=', form.cleaned_data['description'])
            print('3. form country=', form.cleaned_data['country'])
            form.save()
            return render(request, "hbi-dashboard/dashboard.html")
        else:
            return render(request, "hbi-dashboard/dashboard.html")
    context = {'form':form,
               'title': 'Edit Document',
              }
    return render(request, 'hbi-dashboard/edit_document.html', context)


#######################################################################################################

@login_required
def upload_brochure(request):
    my_qs = Member.objects.filter(username=request.user)
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
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
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
    my_qs = Member.objects.filter(username=request.user)
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
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
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
    my_qs = Member.objects.filter(username=request.user)
    # print ('my_qs.powerpoint_country=',my_qs[0].powerpoint_country)
    initial_data = {
        'country': my_qs[0].eproof_country,
    }
    if request.method == 'POST':
        form = EproofForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Eproof, title=form.cleaned_data['title'])
            print('1. object title=', selected_item.title)
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
            selected_item.save()
            return redirect('dashboard')
    else:
        form = EproofForm(initial=initial_data)
        context = {"title": "New Upload E-Proof",
                   "form": form
                   }
    return render(request, 'hbi-dashboard/upload_eproof.html', context)
    #return render(request, 'hbi-dashboard/upload_documents.html', context)


@login_required
def upload_manual(request):
    my_qs = Member.objects.filter(username=request.user)
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
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
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
    my_qs = Member.objects.filter(username=request.user)
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
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
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
    my_qs = Member.objects.filter(username=request.user)
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
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
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
    my_qs = Member.objects.filter(username=request.user)
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
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
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