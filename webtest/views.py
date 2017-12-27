from django.shortcuts import render

# Create your views here.
def new_order(request):
    return render(request, 'webtest/new_order.html')
