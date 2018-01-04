from django.contrib import admin
from .models import States
from .models import Client
from .models import Vendor
from .models import Tracking
from .models import Orders

# Register your models here.
admin.site.register(States)
admin.site.register(Client)
admin.site.register(Vendor)
admin.site.register(Tracking)
admin.site.register(Orders)
