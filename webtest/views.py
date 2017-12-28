from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'webtest/index.html')

def new_order(request):
    return render(request, 'webtest/new_order.html')

def seedfile(request):
    return render(request, 'webtest/seed_file.html')

def nondelivered(request):
    return render(request, 'webtest/non_delivered.html')

def reportsdelivered(request):
    return render(request, 'webtest/reports_delivered.html')
