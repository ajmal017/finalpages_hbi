from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from django.contrib.auth.decorators import login_required
from .models import Listing, Eproof, Product
from members.models import Member
from .forms import EditDocumentForm, UploadDocumentForm
from .forms import UploadEproofForm, UploadBrochureForm, EditBrochureForm

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
    #tasks = Product.objects.all().order_by('-id')
    my_qs = Member.objects.filter(username=request.user)
    tasks = Product.objects.filter(contributor=my_qs[0])
    serializer = ListingSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def mydocumentstaskDetail(request, pk):
    tasks = Product.objects.get(id=pk)
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
    task = Product.objects.get(id=pk)
    serializer = ListingSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        print('Serializer is valid')
        serializer.save()
    else:
        print('ERROR: Serializer is NOT valid')
    return Response(serializer.data)

@api_view(['DELETE'])
def mydocumentstaskDelete(request, pk):
    task = Product.objects.get(id=pk)
    task.delete()
    return Response('Item succsesfully delete!')




@login_required
def mydocumentslist(request):
    if request.user.is_authenticated:
        my_qs = Member.objects.filter(username=request.user)
        qs = Listing.objects.filter(contributor=my_qs[0])
        context = {"title": "HBI List.html", 'my_qs': my_qs}
        return render(request, "hbi-dashboard/list.html", context)

@login_required
def alldocuments(request):
    if request.user.is_authenticated:
        qs = Product.objects.filter(is_published=True)
        context = {"title": "All Documents", 'blog_list': qs }
        return render(request, "hbi-dashboard/alldocuments.html", context)

@login_required
def mydocuments(request):
    if request.user.is_authenticated:
        my_qs = Member.objects.filter(username=request.user)
        #print("*. my_qs[0]", my_qs[0])
        qs = Listing.objects.filter(contributor=my_qs[0])
        #print ('*. qs=',qs)
        context = {"title": "My Documents", 'listing': qs}
        return render(request, "hbi-dashboard/mydocuments.html", context)

@login_required
def selecteddocument(request, listing_id):                 #display individual items
  listing = get_object_or_404(Product, pk=listing_id)
  context = {
    'title': 'Document:',
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

@login_required
def edit_document(request, listing_id):
    selected_document = get_object_or_404(Product, pk=listing_id)
    print ('selected_document.type=', selected_document.type)
    form = EditBrochureForm(instance=selected_document)

    if request.method == 'POST':
        form = EditBrochureForm(request.POST, request.FILES, instance=selected_document)
        if form.is_valid():
            print('1. form title=', form.cleaned_data['title'])
            print('2. form description=', form.cleaned_data['description'])
            form.save()
            return render(request, "hbi-dashboard/dashboard.html")
        else:
            return render(request, "hbi-dashboard/dashboard.html")

    else:
        context = {'form':form,
                   'selected_document': selected_document,
                   'title': 'Edit Document',
                   'subtitle': selected_document.title,
                }
        if selected_document.type == "EPROOF":
            return render(request, 'hbi-dashboard/edit_eproof.html', context)
        else:
            return render(request, 'hbi-dashboard/edit_brochure.html', context)


########################################################################################################################

@login_required
def upload_eproof(request):
    if request.method == 'POST':
        print('at request.method==POST')
        form = UploadEproofForm(request.POST, request.FILES)
        if form.is_valid():
            print('form is valid')
            form.save()
            #selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            print('1. object title=', selected_item.title)
            print('2. object document_file=', selected_item.document_file)
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
            selected_item.cover_file = selected_item.document_file
            selected_item.image1_file = selected_item.document_file
            selected_item.type = 'EPROOF'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadEproofForm()
        context = {"title": "Upload EProof Document",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_eproof.html', context)



@login_required
def upload_brochure(request):
    if request.method == 'POST':
        form = UploadBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]
            selected_item.type = 'BROCHURE'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadBrochureForm()
        context = {"title": "Upload Brochure Document",
                   "type": "Brochure",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_brochure.html', context)

@login_required
def upload_certificate(request):
    if request.method == 'POST':
        form = UploadBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]
            selected_item.type = 'CERTIFICATE'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadBrochureForm()
        context = {"title": "Upload Certificate Document",
                   "type": "Certificate",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_brochure.html', context)

@login_required
def upload_manual(request):
    if request.method == 'POST':
        form = UploadBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]
            selected_item.type = 'MANUAL'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadBrochureForm()
        context = {"title": "Upload Manual Document",
                   "type": "Manual",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_brochure.html', context)

@login_required
def upload_powerpoint(request):
    if request.method == 'POST':
        form = UploadBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]
            selected_item.type = 'POWERPOINT'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadBrochureForm()
        context = {"title": "Upload Powerpoint Document",
                   "type": "Powerpoint",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_brochure.html', context)

@login_required
def upload_proposal(request):
    if request.method == 'POST':
        form = UploadBrochureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Product, title=form.cleaned_data['title'], list_date=form.cleaned_data['list_date'])
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]
            selected_item.type = 'PROPOSAL'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadBrochureForm()
        context = {"title": "Upload Proposal Document",
                   "type": "Proposal",
                   "form": form
                   }
        return render(request, 'hbi-dashboard/upload_brochure.html', context)


##############################################################################################

@login_required
def upload_eproof_OLD(request):
    my_qs = Member.objects.filter(username=request.user)
    # print ('my_qs.powerpoint_country=',my_qs[0].powerpoint_country)
    initial_data = {
        'country': my_qs[0].eproof_country,
    }
    if request.method == 'POST':
        form = UploadEproofForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Eproof, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            print('1. object title=', selected_item.title)
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
            selected_item.save()
            return redirect('home')
    else:
        form = UploadEproofForm(initial=initial_data)
        context = {"title": "Upload E-Proof Document",
                   "form": form
                   }
    return render(request, 'hbi-dashboard/upload_eproof.html', context)
    #return render(request, 'hbi-dashboard/upload_documents.html', context)

@login_required
def upload_brochure_OLD(request):
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            #print('1. object title=', selected_item.title)
            #print('2. object description=', selected_item.description)
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
            selected_item.type = 'BROCHURE'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadDocumentForm()
        context = {"heading": "Upload Brochure Document",
                   "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)

@login_required
def upload_certificate_OLD(request):
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            #print('1. object title=', selected_item.title)
            #print('2. object description=', selected_item.description)
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
            selected_item.type = 'CERTIFICATE'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadDocumentForm()
        context = {"heading": "Upload Certificate Document",
                   "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)

@login_required
def upload_manual_OLD(request):
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            #print('1. object title=', selected_item.title)
            #print('2. object description=', selected_item.description)
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
            selected_item.type = 'MANUAL'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadDocumentForm()
        context = {"heading": "Upload Manual Document",
                   "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)


@login_required
def upload_proposal_OLD(request):
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            #print('1. object title=', selected_item.title)
            #print('2. object description=', selected_item.description)
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
            selected_item.type = 'PROPOSAL'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadDocumentForm()
        context = {"heading": "Upload Proposal Document",
                   "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)

@login_required
def upload_powerpoint_OLD(request):
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            selected_item = get_object_or_404(Listing, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            #print('1. object title=', selected_item.title)
            #print('2. object description=', selected_item.description)
            my_qs = Member.objects.filter(username=request.user)
            selected_item.contributor = my_qs[0]  # assign a Member object into selected_customer.salesrep
            selected_item.type = 'POWERPOINT'
            selected_item.save()
            return redirect('home')
    else:
        form = UploadDocumentForm()
        context = {"heading": "Upload Powerpoint Document",
                   "form": form
                   }
    return render(request, 'hbi-dashboard/upload_documents.html', context)






#BTRE functions ################################################################################################################

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