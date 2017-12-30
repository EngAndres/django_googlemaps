from django import forms
from .models import Orders
from .models import Vendor

def get_vendors():
    temp = Vendor.vendors.get_vendors()
    vendors = ((element[0], element[0]) for element in temp)
    return vendors 


class NewOrder(forms.ModelForm):
    order_number = forms.CharField(label = "Order Number", required=True)
    vendor = forms.ChoiceField(label = "Associated Vendor", required=True, choices=get_vendors())
    tracking_number = forms.CharField(label = "Tracking Number", required=True)
    shipping_address = forms.CharField(label = "Shipping Address", required=True)

    class Meta:
        model = Orders
        fields = ('order_number','tracking_number','shipping_address')  

class UploadFile(forms.Form):
    file_upload = forms.FileField(label = "Select File")
	
        

