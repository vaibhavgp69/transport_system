from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import uuid #generates unique id 
from datetime import datetime


User = get_user_model()


class TransportOffice(models.Model):
    point_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    time = models.TimeField()
    date = models.DateField()
        
    def __str__(self):
        return "Name : " + self.name + "  Point id: " + str(self.point_id)
    
class RegisteredCustomer(models.Model):
    c_id = models.IntegerField(primary_key=True)
    c_name = models.CharField(max_length=100)
    c_add = models.CharField(max_length=255)
    mob_no = models.CharField(max_length=15)

    def __str__(self):
        return f"Name: {self.c_name}, ID: {self.c_id}"

class Taxi(models.Model):
    t_id = models.IntegerField(primary_key=True)
    c_id = models.ForeignKey(RegisteredCustomer, on_delete=models.CASCADE)
    point_id = models.ForeignKey(TransportOffice, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    capacity = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Taxi ID: {self.t_id}, Type: {self.type}, Capacity: {self.capacity}"

class BaseStation(models.Model):
    b_id = models.IntegerField(primary_key=True)
    point_id = models.ForeignKey(TransportOffice, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    loc = models.CharField(max_length=255)
    src = models.CharField(max_length=255)
    dest = models.CharField(max_length=255)

    def __str__(self):
        return f"Base Station ID: {self.b_id}, Name: {self.name}, Location: {self.loc}"

class RouteDetails(models.Model):
    r_no = models.IntegerField(primary_key=True)
    src = models.CharField(max_length=255)
    dest = models.CharField(max_length=255)
    point_id = models.ForeignKey(TransportOffice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Route Number: {self.r_no}, Source: {self.src}, Destination: {self.dest}"
    
# Relationships defined below 

class Registration(models.Model):
    point_id = models.ForeignKey(TransportOffice, on_delete=models.CASCADE)
    t_id = models.ForeignKey(Taxi, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['point_id', 't_id'], name='unique_registration')
        ]

    def __str__(self):
        return f"Transport Office: {self.point_id}, Taxi ID: {self.t_id}"

class Request(models.Model):
    src = models.CharField(max_length=255)
    dest = models.CharField(max_length=255)
    time = models.TimeField()
    date = models.DateField()
    c_id = models.ForeignKey(RegisteredCustomer, on_delete=models.CASCADE)
    point_id = models.ForeignKey(TransportOffice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Request: Source: {self.src}, Destination: {self.dest}, Time: {self.time}, Date: {self.date}, Customer ID: {self.c_id}"


