from django import forms
from .models import Orders
from .models import Vendor


class NewOrder(forms.ModelForm):
    temp = Vendor.vendors.get_vendors()
    vendors = ((element[1], element[1]) for element in temp) 

    order_number = forms.CharField(label = "Order Number", required=True)
    vendor = forms.ChoiceField(label = "Associated Vendor", required=True, choices=vendors)
    tracking_number = forms.CharField(label = "Tracking Number", required=True)
    shipping_address = forms.CharField(label = "Shipping Address", required=True)

    class Meta:
        model = Orders
        fields = ('order_number','vendor','tracking_number','shipping_address')  


class UploadFile(forms.Form):
    file_upload = forms.FileField(label = "Select File")


class ReportFilter(forms.Form):
    temp = Vendor.vendors.get_vendors()
   
    vendors = ()
    vendors += (('-1', "(All vendors)"),)
    for element in temp:
        vendors += ((element[0], element[1]),)
    vendor = forms.ChoiceField(label = "Associated Vendor", required=False, choices=vendors)    
    
    states =  (('1', "(All states)"),('3', "Delivered"),('4', "Normal Non-Delivered"),('5', "Late Non-Delivered"),('6', "Very Late Non-Delivered"),)
    state = forms.ChoiceField(label = "Shipping State", required=False, choices=states)
    
    #created_date = forms.DateField(label = "Created Date", required=False)
    #delivered_date = forms.DateField(label = "Delivered Date", required=False)







