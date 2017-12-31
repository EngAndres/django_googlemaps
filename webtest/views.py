from django.shortcuts import render
from .models import Orders
from .models import Client
from .models import States
from .models import Vendor
from django.http import HttpResponseRedirect
from geopy.geocoders import Nominatim
from .forms import NewOrder
from .forms import UploadFile

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



def upload_seed_file(file_):
    for line in file_:
        order = str(line).split("'")[1].split(",")
        order_number_ = order[0]
        tracking_number_ = order[3]
        vendor_ = order[1]
        client_ = '1'
        shipping_address_ = order[4].replace("\\r\\n", "")

        geolocator = Nominatim()
        location = geolocator.geocode( shipping_address_ )

        if location is not None:
            shipping_latitude_ = location.latitude
            shipping_longitude_ = location.longitude
        else:
            shipping_latitude_ = '0.0'
            shipping_longitude_ = '0.0'
		
        state_ = order[2]
        
        order = Orders.orders.insert_order(order_number_, tracking_number_, Vendor.objects.get(id = vendor_), Client.objects.get(id = client_), shipping_address_, shipping_latitude_, shipping_longitude_, States.objects.get(id =  state_))
        order.save()




def seedfile(request):
    if request.method == 'POST':
        frmUploadFile = UploadFile(request.POST, request.FILES)

        if frmUploadFile.is_valid():
            upload_seed_file(request.FILES['file_upload'])
            
        	    
    frmUploadFile = UploadFile()


    return render(request, 'webtest/seed_file.html',{'frmUploadFile':frmUploadFile})






def nondelivered(request):
    temp = Orders.orders.get_orders_non_delivered()
    orders = [{'id':element[0], 'order_num':element[1], 'vendor':element[2], 'client':element[3], 'address':element[4], 'created':element[5]} for element in temp]    
    return render(request, 'webtest/non_delivered.html',{'orders':orders})




def reportsdelivered(request):
    temp = Orders.orders.get_orders_delivered()
    orders = [{'id':element[0], 'order_num':element[1], 'vendor':element[2], 'client':element[3], 'address':element[4], 'delivered':element[5]} for element in temp]
    return render(request, 'webtest/reports_delivered.html',{'orders':orders})






