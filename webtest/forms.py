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

from django import forms
from .models import Orders
from .models import Vendor


#This is a form to save information about a new order
class NewOrder(forms.ModelForm):
    temp = Vendor.vendors.get_vendors()
    vendors = ((element[1], element[1]) for element in temp)  #Create a list of all registered vendors 

    order_number = forms.CharField(label = "Order Number", required=True)
    vendor = forms.ChoiceField(label = "Associated Vendor", required=True, choices=vendors)
    tracking_number = forms.CharField(label = "Tracking Number", required=True)
    shipping_address = forms.CharField(label = "Shipping Address", required=True)

    class Meta:
        model = Orders #Form based on Orders model
        fields = ('order_number','vendor','tracking_number','shipping_address')  



#This is a simple form to upload a seed file
class UploadFile(forms.Form):
    file_upload = forms.FileField(label = "Select File")



#This is a form used to define filters in reports generation
class ReportFilter(forms.Form):
    #Create a ComboBox of associated vendors
    temp = Vendor.vendors.get_vendors()
    vendors = () #Create a list
    vendors += (('-1', "(All vendors)"),) #Add the default value of ComboBox
    for element in temp:
        vendors += ((element[0], element[1]),) #Add each vendor registered in database
    vendor = forms.ChoiceField(label = "Associated Vendor", required=False, choices=vendors)    
    
    states =  (('1', "(All states)"),('3', "Delivered"),('4', "Normal Non-Delivered"),('5', "Late Non-Delivered"),('6', "Very Late Non-Delivered"),) #Create a list of all available states of shipping
    state = forms.ChoiceField(label = "Shipping State", required=False, choices=states)
    
    #created_date = forms.DateField(label = "Created Date", required=False)
    #delivered_date = forms.DateField(label = "Delivered Date", required=False)
