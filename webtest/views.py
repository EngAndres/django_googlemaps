from django.shortcuts import render
from .models import Orders
from .models import Client
from .models import States
from .models import Vendor
from django.http import HttpResponseRedirect
from geopy.geocoders import Nominatim
from .forms import NewOrder
from .forms import UploadFile
from .forms import ReportFilter
import time

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
        time.sleep(0.1)



def seedfile(request):
    if request.method == 'POST':
        frmUploadFile = UploadFile(request.POST, request.FILES)

        if frmUploadFile.is_valid():
            upload_seed_file(request.FILES['file_upload'])
        	    
    frmUploadFile = UploadFile()

    return render(request, 'webtest/seed_file.html',{'frmUploadFile':frmUploadFile})






def nondelivered_list(request):
    temp = Orders.orders.get_orders_non_delivered()
    orders = [{'id':element[0], 'order_num':element[1], 'vendor':element[2], 'client':element[3], 'address':element[4], 'created':element[5], 'latitude':element[6], 'longitude':element[7], 'vendor_id':element[8], 'time':element[9]} for element in temp]    

    for order in orders:
        average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])


        if average[0][0] is None:
            order['delay'] = "---"
        else:
            factor = order['time'] / average[0][0]
            if factor < 1.0:
                order['delay'] = "Normal"
            else:
                if factor < 1.25:
                    order['delay'] = "Not Normal"
                else:
                    order['delay'] = "Very Late"
        
    return render(request, 'webtest/non_delivered.html',{'orders':orders})



def nondelivered_map(request):
    temp = Orders.orders.get_orders_non_delivered()
    orders = [{'id':element[0], 'order_num':element[1], 'vendor':element[2], 'client':element[3], 'address':element[4], 'created':element[5], 'latitude':element[6], 'longitude':element[7], 'vendor_id':element[8], 'time':element[9]} for element in temp]    

    for order in orders:
        average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])


        if average[0][0] is None:
            order['delay'] = "---"
        else:
            factor = order['time'] / average[0][0]
            if factor < 1.0:
                order['delay'] = "Normal"
            else:
                if factor < 1.25:
                    order['delay'] = "Not Normal"
                else:
                    order['delay'] = "Very Late"
        
    return render(request, 'webtest/non_delivered_maps.html',{'orders':orders})




def reports(request):
    if request.method == 'POST':
        frmReports = ReportFilter(request.POST)

        type_ = 1
        constraint = ""

        if frmReports.is_valid():
            vendor = request.POST.get("vendor")
            state = request.POST.get("state")
            #delivered = request.POST.get("delivered_date")
            #created = request.POST.get("created_date")

            
            if vendor != '-1':
                constraint += " webtest_orders.vendor_fk_id = " + vendor
            
            if state != '1':
                type_ = state
                if len(constraint) != 0:
                    constraint += " AND "
                if state == '3':
                    constraint += " webtest_orders.state_fk_id = " + state
                else:
                    constraint += " webtest_orders.state_fk_id = 1 OR  webtest_orders.state_fk_id = 2 "

            #if delivered is None:
              #  if len(constraint) != 0:
               #     constraint += " AND "

               # constraint += " webtest_orders.deliverated_date = " + delivered

          #  if created is None:
           #     if len(constraint) != 0:
            #        constraint += " AND "

             #   constraint += " webtest_orders.created_date = " + created

            if len(constraint) > 0:
                constraint = " WHERE " + constraint

        parameter = []
        temp = Orders.orders.get_orders_by_constraint(constraint)
        orders_ = [{'id':element[0], 'order_num':element[1], 'vendor':element[2], 'client':element[3], 'address':element[4], 'created':element[5], 'delivered':element[6], 'time':element[7], 'latitude':element[8], 'longitude':element[9], 'vendor_id':element[10]} for element in temp]    

        if  type_ == 1 or type_ == '3':
            for order in orders_:
                if order['delivered'] is None:                
                    average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])

                    factor = 0 if average[0][0] is None else order['time'] / average[0][0]
                    if factor < 1.0:
                        order['delivered'] = "Normal"
                    else:
                        if factor < 1.25:
                            order['delivered'] = "Not Normal"
                        else:
                            order['delivered'] = "Very Late"
            parameter = []
            parameter = orders_
        else:
            if type_ != '3':
                parameter = []            
                if type_ == '4':
                    for order in orders_:
                        average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])

                        factor = 0 if average[0][0] is None else order['time'] / average[0][0]
                        if factor < 1.0:
                             order['delivered'] = "Normal"
                             parameter.append(order)
                else:  
                    if type_ == '5':
                        for order in orders_:
                            average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])

                            factor = 0 if average[0][0] is None else order['time'] / average[0][0]
                            if factor < 1.25 and factor >= 1.0:
                                order['delivered'] = "Not Normal"
                                parameter.append(order)
                    else:
                        for order in orders_:
                            average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])

                            factor = 0 if average[0][0] is None else order['time'] / average[0][0]
                            if factor >= 1.25:
                                order['delivered'] = "Very Late"
                                parameter.append(order)

        return render(request, 'webtest/reports_.html',{'orders':parameter, 'type':type_})
    else:
        frmReports = ReportFilter()

        return render(request, 'webtest/reports.html',{'frmReports':frmReports})    	




