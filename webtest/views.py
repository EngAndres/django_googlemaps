'''
# Solution for Software Delevopment Test.
#
# Created by MSc. Carlos Andres Sierra on February 2018.
# Copyright (c) 2018  Msc. Carlos Andres Sierra.  All rights reserved.
#
# This file is part of NegotiatusDashboardProject.
#
# NegotiatusDashboardProject is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3.
'''

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Orders
from .models import Client
from .models import States
from .models import Vendor
from .forms import NewOrder
from .forms import UploadFile
from .forms import ReportFilter
from geopy.geocoders import Nominatim
import time

#this is a factor used to define if an order has taking more time than normal to be delivered
factor_very_late = 1.25


# Index View. In this method the view load the default web page of this app.
def index(request):
    return render(request, 'webtest/index.html')



# New Order View. In this method there are two options: show a clean form to add an order, or receive a form with data
# to process and send to database.
def new_order(request):
    if request.method == 'POST': #verify if a form has been sent
        frmNewOrder = NewOrder(request.POST) #save data from the form

        if frmNewOrder.is_valid(): #avoid errors
            geolocator = Nominatim() #object to work with geoposition
            
            #save current information of the form. Commit is false because more information will be added to the model.
            order = frmNewOrder.save(commit=False) 
            order.client_fk = Client.objects.get(id = '1') #add a valid client 
            
            #get geographic information based on the given address
            location = geolocator.geocode( request.POST.get("shipping_address") ) 

            #There are issues with the address, and if GeoPy can't process the address (no valid format), 
            #it returns a None value
            if location is not None:
                order.shipping_latitude = location.latitude
                order.shipping_longitude = location.longitude
            else: #logic invalid values to latitude and longitude are defined, this must be fixed trying to standarize the address in the form
                order.shipping_latitude = '0.0'
                order.shipping_longitude = '0.0'

            order.state_fk = States.objects.get(id = '1') #add "In Factory" state to the new order
            order.vendor_fk = Vendor.objects.get(name = request.POST.get("vendor")) #add the complete object of vendor

            order.save() #send order information to the database
    #end if    	    
        
    frmNewOrder = NewOrder() #create a new form to be send at the webpage

    #call the webpage for a new order, and send a clean form as parameter
    return render(request, 'webtest/new_order.html',{'frmNewOrder':frmNewOrder})



#This method is used to process a file with a data-structure defined and seed the database with each register in the file
def upload_seed_file(file_):
    for line in file_: #move by each line of the file
        order = str(line).split("'")[1].split(",") #remove meta of the file that is not useful
        
        #for this example, it is assumed a data-structure as follows: order_number,vendor_id,state_id,tracking_number,shipping_address 
        order_number_ = order[0] 
        vendor_ = order[1]
        state_ = order[2]
        tracking_number_ = order[3]
        shipping_address_ = order[4].replace("\\r\\n", "") #remove tags for end of line
        client_ = '1' #generic client defined for this version
        
        geolocator = Nominatim() #object to work with geoposition
        
        #get geographic information based on the given address
        location = geolocator.geocode( shipping_address_ )

        #There are issues with the address, and if GeoPy can't process the address (no valid format), 
        #it returns a None value
        if location is not None: #assign right coordenates information
            shipping_latitude_ = location.latitude
            shipping_longitude_ = location.longitude
        else: #logic invalid values to latitude and longitude are defined, this must be fixed trying to standarize the address in the form
            shipping_latitude_ = '0.0'
            shipping_longitude_ = '0.0'
		
        
        #Once all register information is set, it is time to save this register in the database
        order = Orders.orders.insert_order(order_number_, tracking_number_, Vendor.objects.get(id = vendor_), Client.objects.get(id = client_), shipping_address_, shipping_latitude_, shipping_longitude_, States.objects.get(id =  state_))
        order.save()
        time.sleep(0.15) #This delay try to avoid the problem of saturate GeoPy service. TODO improve it



#Seed file view. In this method we request a file to the user, this file has seed information to seed the database.
def seedfile(request):
    if request.method == 'POST': #verify if a form has been sent
        frmUploadFile = UploadFile(request.POST, request.FILES) #save information of the form, in this case, the file uploaded.

        if frmUploadFile.is_valid(): #avoid errors
            upload_seed_file(request.FILES['file_upload']) #call to funtion to process the uploaded file
        	    
    frmUploadFile = UploadFile() #create a new form to be send as parameter of the view

    return render(request, 'webtest/seed_file.html',{'frmUploadFile':frmUploadFile})



# This method is used to define a delay classification based on a factor of the shipping time for the current order and 
# the average time spent on past deliveries made by a specific vendor to the given address (and a small neighborhood around it) 
def calculate_delay(factor):
    if factor <= 1.0: #It is inside an average time
        return "Normal"
    else:
        if factor < factor_very_late:
            return "Not Normal" #It is more late than average time but it's acceptable
        else:
            return "Very Late" #It is later than average time and it isn't acceptable    



#Non-delivered list view. In this method is building a list of a non-delivered orders, and the list is sent to a 
#web page to be showed in a table.
def nondelivered_list(request):
    temp = Orders.orders.get_orders_non_delivered() #call to a query that returns all orders that has not been delivered
   
    #save query information in an array of Python dictionaries; one dictionary per each order
    orders = [{'id':element[0], 'order_num':element[1], 'vendor':element[2], 'client':element[3], 'address':element[4], 'created':element[5], 'latitude':element[6], 'longitude':element[7], 'vendor_id':element[8], 'time':element[9]} for element in temp]    

    for order in orders: #move by each order
        #Call to a query that get an average delivered time between a vendor and a defined geographic location (even a little neighborhood)s
        average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])

        #If there is not coincidences of previous deliveries of the vendor and the location given, query result will be "None"
        if average[0][0] is None:
            order['delay'] = "---" #There is no message to show 
        else:
            #There are previous coincidences
            #A factor is defined to compare the average time with the delivery time with the current orders
            factor = order['time'] / average[0][0] #This is a simple way to make a correlation between these values
            order['delay'] = calculate_delay(factor) #Call to a function that returns a message based on the factor obtained
        
    return render(request, 'webtest/non_delivered.html',{'orders':orders})



#
def define_icon(delay):
    if delay == "Normal":
        return "https://raw.githubusercontent.com/EngAndres/negotiatus_test/master/webtest/static/webtest/images/icons/green_map-marker.png"
    else:
        if delay == "Not Normal":
            return "https://raw.githubusercontent.com/EngAndres/negotiatus_test/master/webtest/static/webtest/images/icons/orange_map-marker.png"
        else:
            return "https://raw.githubusercontent.com/EngAndres/negotiatus_test/master/webtest/static/webtest/images/icons/red_map-marker.png"




#Non-delivered list view. In this method is building a list of a non-delivered orders, and the list is sent to a 
#web page to be showed in a table.
def nondelivered_map(request):
    temp = Orders.orders.get_orders_non_delivered()
    orders = [{'id':element[0], 'order_num':("Order Number: "+ str(element[1])), 'vendor':("Vendor: " + element[2]), 'client':element[3], 'address':("Address: " + element[4]), 'created':element[5], 'latitude':element[6], 'longitude':element[7], 'vendor_id':element[8], 'time':element[9]} for element in temp]    

    for order in orders:
        average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])

        factor = 0 if average[0][0] is None else order['time'] / average[0][0]
        order['delay'] = calculate_delay(factor)
        order['icon'] = define_icon(order['delay'])
        
    return render(request, 'webtest/non_delivered_maps.html',{'orders':orders})




#
def orders_filtered(constraint, type_):
    temp = Orders.orders.get_orders_by_constraint(constraint)
    orders_ = [{'id':element[0], 'order_num':element[1], 'vendor':element[2], 'client':element[3], 'address':element[4], 'created':element[5], 'delivered':element[6], 'time':element[7], 'latitude':element[8], 'longitude':element[9], 'vendor_id':element[10]} for element in temp]    

    if  type_ == 1 or type_ == '3':
        for order in orders_:
            if order['delivered'] is None:                
                average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])

                factor = 0 if average[0][0] is None else order['time'] / average[0][0]
                order['delivered'] = calculate_delay(factor)

        return orders_
    else:
        filtered = []            
        if type_ == '4':
            for order in orders_:
                average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])

                factor = 0 if average[0][0] is None else order['time'] / average[0][0]
                if factor < 1.0:
                     order['delivered'] = "Normal"
                     filtered.append(order)
        else:  
            if type_ == '5':
                for order in orders_:
                    average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])

                    factor = 0 if average[0][0] is None else order['time'] / average[0][0]
                    if factor < factor_very_late and factor >= 1.0:
                        order['delivered'] = "Not Normal"
                        filtered.append(order)
            else:
                for order in orders_:
                    average = Orders.orders.get_orders_average_time(order['vendor_id'], order['latitude'], order['longitude'])

                    factor = 0 if average[0][0] is None else order['time'] / average[0][0]
                    if factor >= factor_very_late:
                        order['delivered'] = "Very Late"
                        filtered.append(order)
        return filtered



#
def reports(request):
    if request.method == 'POST':
        frmReports = ReportFilter(request.POST)

        type_ = 1
        constraint = ""

        if frmReports.is_valid():
            vendor = request.POST.get("vendor")
            state = request.POST.get("state")
      
            
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

            if len(constraint) > 0:
                constraint = " WHERE " + constraint

        orders = orders_filtered(constraint, type_)         

        return render(request, 'webtest/reports_.html',{'orders':orders, 'type':type_})
    else:
        frmReports = ReportFilter()

        return render(request, 'webtest/reports.html',{'frmReports':frmReports})   
