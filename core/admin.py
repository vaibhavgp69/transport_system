
from django.contrib import admin
from .models import TransportOffice, RegisteredCustomer, Taxi, BaseStation, RouteDetails, Registration, Request

admin.site.register(TransportOffice)
admin.site.register(RegisteredCustomer)
admin.site.register(Taxi)
admin.site.register(BaseStation)
admin.site.register(RouteDetails)
admin.site.register(Registration)
admin.site.register(Request)

