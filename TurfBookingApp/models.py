from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True)
    def __str__(self):
        return str(self.user) + " ["+str(self.phone)+"]"

class Turf(models.Model):
    turf_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=500, blank=True)
    charges = models.IntegerField()
    image = models.ImageField(upload_to="", blank=True)

    def __str__(self):
        return "["+str(self.turf_name)+"]["+str(self.phone)+"]["+str(self.address)+"]["+str(self.description)+"]"

class Booking(models.Model):
    booking_date = models.CharField(max_length=50)
    for_date = models.CharField(max_length=50)
    for_time = models.CharField(max_length=50)
    charges = models.IntegerField()
    card_no = models.CharField(max_length=20)
    card_holder = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    def __str__(self):
        return "["+str(self.booking_date)+","+str(self.for_date)+","+str(self.for_time)+","+str(self.charges)+","+str(self.card_no)+","+str(self.card_holder)+","+str(self.bank_name)+","+str(self.customer)+"]"

class Feedback(models.Model):
    feedback_date = models.DateField(max_length=50, default=datetime.now())
    feedback_message = models.CharField(max_length=500)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return "["+str(self.feedback_date)+","+str(self.feedback_message)+","+str(self.customer)+"]"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.CharField(max_length=400)

    def __str__(self):
        return "["+str(self.name)+","+str(self.email)+","+str(self.phone)+","+str(self.message)+"]"