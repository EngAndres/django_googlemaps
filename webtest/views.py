from django.shortcuts import render
from .models import Orders
from .models import Client
from .models import States
from .models import Vendor
from .models import OrdersManager
from django.http import HttpResponseRedirect
from geopy.geocoders import Nominatim
from .forms import NewOrder

# Create your views here.
def index(request):
    return render(request, 'webtest/index.html')

def new_order(request):
    if request.method == 'POST':
        frmNewOrder = NewOrder(request.POST)


        if frmNewOrder.is_valid():
            geolocator = Nominatim()
            order = frmNewOrder.save(commit=False)
            order.client_fk = Client.objects.get(id = '1') 
            location = geolocator.geocode( request.POST.get("shipping_address") )

            if location is not None:
                order.shipping_latitude = location.latitude
                order.shipping_longitude = location.longitude
            else:
                order.shipping_latitude = '0.0'
                order.shipping_longitude = '0.0'

            order.state_fk = States.objects.get(id = '1')
            order.vendor_fk = Vendor.objects.get(name = request.POST.get("vendor"))


            order.save()
        	    
    
    frmNewOrder = NewOrder()

    return render(request, 'webtest/new_order.html',{'frmNewOrder':frmNewOrder})


def adding_order(request):
    if request.method == 'POST':
        order_number = request.POST.get('txtOrder')	
        associated_vendor = request.POST.get('cbxVendor')
        tracking_number = request.POST.get('txtTracking')
        address_shipping = request.POST.get('txtAddress')

        return HttpResponseRedirect('../adding_order/',{'order_number':order_number})
            
        
    return render(request, 'webtest/new_order.html')

def seedfile(request):
    return render(request, 'webtest/seed_file.html')

def nondelivered(request):
    return render(request, 'webtest/non_delivered.html')

def reportsdelivered(request):
    orders = Orders.orders.get_orders_delivered()
    return render(request, 'webtest/reports_delivered.html',{'orders':orders})
