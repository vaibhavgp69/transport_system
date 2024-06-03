from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),    
     path('transport', views.transport_office_create, name='transport'),
     path('request', views.c_request, name='request'),
     path('taxi', views.taxi_form, name='taxi'),
      path('booktaxi', views.book_taxi, name='booktaxi'),
       path('basestation/', views.basestation, name='basestation'),
        path('route/', views.route, name='route'),
       path('logout', views.logout, name='logout'),
    
]