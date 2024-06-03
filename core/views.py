from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages 
from .models import TransportOffice, RegisteredCustomer, Taxi, BaseStation, RouteDetails, Registration, Request
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from datetime import datetime
from itertools import chain
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Subquery
from django.db.models import Count
import random 
from django.http import JsonResponse
import uuid

def index(request):
    registered_taxis_ids = Registration.objects.values_list('t_id', flat=True)
    transport_offices = TransportOffice.objects.all()[:5]
    transport_offices = transport_offices.annotate(num_basestations=Count('basestation'))
    available_taxis = Taxi.objects.exclude(pk__in=Subquery(registered_taxis_ids))[:5]

    return render(request, 'index.html', {'transport_offices': transport_offices, 'taxis': available_taxis})

def logout(request):
    auth.logout(request)
    return redirect('signin')
    messages.info(request, 'You have been logged out')

def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pw']
        password2 = request.POST['pw2'] 
        adress = request.POST['adress']
        mobile_no = request.POST['mobile']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_id = user.id
                registered_customer = RegisteredCustomer(
                    c_id = user_id,
                    c_name=username,  
                    c_add=adress,    
                    mob_no=mobile_no  
                )
                registered_customer.save()

  
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('signin')
                
        else:
            messages.info(request, 'Password Not matching')
            return  redirect('signup')
        
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['pw']
        
        user=auth.authenticate( username=username , password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    
def transport_office_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        time = request.POST.get('time')
        date = request.POST.get('date')

        if not (name and time and date):
            messages.info(request, 'All fields are required')
            return redirect('transport')

        try:
    
            datetime_object = datetime.strptime(date, '%Y-%m-%d')
          
            transport_office = TransportOffice.objects.create(name=name, time=time, date=date)
            messages.info(request, 'Transport office created successfully')
            return redirect('transport')

        except Exception as e:
         
            messages.info(request, f'An error occurred: {str(e)}')
            return redirect('transport')

    return render(request, 'transport_office_form.html')


@login_required
def c_request(request):
    if request.method == 'POST':
        src = request.POST['src']
        dest = request.POST['dest']
        time = request.POST['time']
        date = request.POST['date']
        c_id = RegisteredCustomer.objects.get(pk=request.user.id) 

        try:
            point_id = request.POST['point_id']
            transport_office = TransportOffice.objects.get(pk=point_id)
        except:
            return render(request, 'request', {'error_message': 'Invalid Transport Office selected.'})

     
        new_request = Request(src=src, dest=dest, time=time, date=date, c_id=c_id, point_id=transport_office)
        new_request.save()
        return redirect('request')  
    else:
        transport_offices = TransportOffice.objects.all()
        return render(request, 'request.html', {'transport_offices': transport_offices})
    
@login_required
def taxi_form(request):
    if request.method == 'POST':
        taxi_type = request.POST['type']
        capacity = request.POST['capacity']
        cost = request.POST['cost']
        c_id = RegisteredCustomer.objects.get(pk=request.user.id) 

        try:
            point_id = request.POST['point_id']
            transport_office = TransportOffice.objects.get(pk=point_id)
        except TransportOffice.DoesNotExist:
            return render(request, 'taxi.html', {'error_message': 'Invalid Transport Office selected.', 'transport_offices': TransportOffice.objects.all()})

        # Create the Taxi object
        new_taxi = Taxi(type=taxi_type, capacity=capacity, cost=cost, c_id=c_id, point_id=transport_office)
        new_taxi.save()
        return redirect('index')  
    else:
        transport_offices = TransportOffice.objects.all()
        return render(request, 'taxi.html', {'transport_offices': transport_offices})

@login_required   
def book_taxi(request):
    if request.method == 'POST':
        point_id = request.POST.get('point_id')
        t_id = request.POST.get('t_id')

      
        taxi_point_id = Taxi.objects.get(pk=t_id).point_id_id
        reg_point_id = TransportOffice.objects.get(point_id=point_id)


        if Registration.objects.filter(point_id=reg_point_id, t_id=t_id).exists():
            messages.info(request, 'The selected combination is already registered.')
            return HttpResponseRedirect(reverse('booktaxi'))

        date = request.POST.get('date')
        time = request.POST.get('time')
        registration = Registration(point_id=reg_point_id, t_id_id=t_id, date=date, time=time)
        registration.save()
        messages.success(request, 'Taxi booked successfully!')
        return HttpResponseRedirect(reverse('booktaxi'))


    transport_offices = TransportOffice.objects.all()
  
    registered_taxis_ids = Registration.objects.values_list('t_id', flat=True)
   
    available_taxis = Taxi.objects.exclude(pk__in=Subquery(registered_taxis_ids))
    return render(request, 'booktaxi.html', {'transport_offices': transport_offices, 'taxis': available_taxis})

@login_required 
def basestation(request):
    if request.method == 'POST':
        point_id = request.POST.get('point_id')
        name = request.POST.get('name')
        loc = request.POST.get('loc')
        src = request.POST.get('src')
        dest = request.POST.get('dest')


        try:
            transport_office = TransportOffice.objects.get(pk=point_id)
        except TransportOffice.DoesNotExist:
            messages.error(request, 'Invalid Transport Office selected.')
            return redirect('basestation')

    
        base_station = BaseStation(point_id=transport_office, name=name, loc=loc, src=src, dest=dest)
        base_station.save()

        messages.success(request, 'Base Station added successfully!')
        return redirect('basestation')


    transport_offices = TransportOffice.objects.all()
    return render(request, 'basestation.html', {'transport_offices': transport_offices})


def route(request):
    if request.method == 'POST':
        point_id = request.POST.get('point_id')
        src = request.POST.get('src')
        dest = request.POST.get('dest')


        try:
            transport_office = TransportOffice.objects.get(pk=point_id)
        except TransportOffice.DoesNotExist:
            messages.error(request, 'Invalid Transport Office selected.')
            return redirect('route')


        route = RouteDetails(point_id=transport_office, src=src, dest=dest)
        route.save()

        messages.success(request, 'Route details added successfully!')
        return redirect('route')


    transport_offices = TransportOffice.objects.all()
    return render(request, 'route.html', {'transport_offices': transport_offices})

