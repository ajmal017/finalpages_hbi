from django.shortcuts import render, get_object_or_404
from .forms import EditCustomerForm
from .models import Customer

def edit_customer(request, customer_id):
    selected_customer = get_object_or_404(Customer, pk=customer_id)
    form = EditCustomerForm(instance=selected_customer)

    if request.method == 'POST':
        print('At form POST')
        form = EditCustomerForm(request.POST, request.FILES, instance=selected_customer)
        if form.is_valid():
            print('form is valid')
            form.save()
            return render(request, "hbi-dashboard/dashboard.html")
        else:
            print ('form is not saved')
            print ('form errors=,',form.errors)
            return render(request, "hbi-dashboard/dashboard.html")
    print('HERE!')
    context = {'form':form,
               'title': 'My Customer',
               'customer': selected_customer
              }
    return render(request, 'hbi-dashboard/edit_customer.html', context)


def mycustomers(request):
    my_customers = Customer.objects.filter(salesrep=request.user)
    #print ('mycustomers =',my_customers)

    context = {
                'title': 'My Customers',
                'my_customers' : my_customers,
              }
    return render(request, 'hbi-dashboard/mycustomerlist.html', context)
