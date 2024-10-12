from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
import re
# Create your views here.
def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']

        t = Contact.objects.create(name = name, phone=phone, email=email, message=message)
        t.save()
        alert = True
        return render(request, "contact.html", {'alert':alert})
    return render(request, "contact.html")

def adminlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/admindashboard")
        else:
            alert = True
            return render(request, "admin-login.html", {'alert':alert})
    return render(request, "admin-login.html")


@login_required(login_url = '/adminlogin')
def admindashboard(request):
    n = Customer.objects.all().count()
    m = Turf.objects.all().count()
    f = Feedback.objects.all().count()
    b = Booking.objects.all().count()
    c = Contact.objects.all().count()
    return render(request, "admin-dashboard.html", {"users": n, "turfs": m, "feedbacks": f, "bookings": b, "contacts": c})

def user_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['pwd']
        confirm_password = request.POST['cpwd']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "user-register.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        customer = Customer.objects.create(user=user, phone=phone)
        user.save()
        customer.save()
        alert = True
        return render(request, "user-register.html", {'alert':alert})
    return render(request, "user-register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a customer!!")
            else:
                t = Customer.objects.get(user_id=user.id)
                request.session['cid'] = t.id
                return redirect("/userdashboard")
        else:
            alert = True
            return render(request, "user-login.html", {'alert':alert})
    return render(request, "user-login.html")

@login_required(login_url = '/user_login')
def userdashboard(request):
    return render(request, "user-dashboard.html")

def Logout(request):
    logout(request)
    return redirect ("/")

@login_required(login_url = '/adminlogin')
def users(request):
    customers = Customer.objects.all()
    return render(request, "view-all-users.html", {'customers':customers})

@login_required(login_url = '/adminlogin')
def delete_user(request, myid):
    c = Customer.objects.get(id=myid)
    c.delete()
    return redirect("/users")

@login_required(login_url = '/adminlogin')
def delete_feedback(request, myid):
    f = Feedback.objects.get(id=myid)
    f.delete()
    return redirect("/feedback")

@login_required(login_url = '/adminlogin')
def view_user_details(request, myid):
    c = Customer.objects.get(id=myid)
    return render(request, "view-user-details.html", {'customer':c})

@login_required(login_url = '/adminlogin')
def turfs(request):
    turf = Turf.objects.all()
    return render(request, "view-all-turfs.html", {'turfs':turf})

@login_required(login_url = '/adminlogin')
def view_turf_details(request, myid):
    t = Turf.objects.get(id=myid)
    return render(request, "view-turf-details.html", {'turf':t})

@login_required(login_url = '/adminlogin')
def delete_turf(request, myid):
    t = Turf.objects.get(id=myid)
    t.delete()
    return redirect("/turfs")

@login_required(login_url = '/adminlogin')
def add_turf(request):
    if request.method == "POST":
        turf_name = request.POST['turf_name']
        phone = request.POST['phone']
        address = request.POST['address']
        description = request.POST['description']
        charges = request.POST['charges']
        image = request.FILES['image']

        t = Turf.objects.create(turf_name = turf_name, phone=phone, address=address, description = description, charges=charges, image=image)
        t.save()
        alert = True
        return render(request, "add-turf.html", {'alert':alert})
    return render(request, "add-turf.html")

@login_required(login_url = '/adminlogin')
def edit_turf(request, myid):
    t = Turf.objects.get(id=myid)
    if request.method == "POST":
        t.turf_name = request.POST['turf_name']
        t.phone = request.POST['phone']
        t.address = request.POST['address']
        t.description = request.POST['description']
        t.charges = request.POST['charges']
        if 'image' in request.FILES:
            t.image = request.FILES['image']
        t.save()

        alert = True
        return render(request, "edit-turf.html", {'alert':alert})
    return render(request, "edit-turf.html", {'turf':t})

@login_required(login_url = '/user_login')
def user_profile(request):
    return render(request, "user-profile.html")

@login_required(login_url = '/user_login')
def user_edit_profile(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == "POST":
        customer.user.first_name = request.POST['first_name']
        customer.user.last_name = request.POST['last_name']
        customer.user.email = request.POST['email']
        customer.phone = request.POST['phone']
        if re.match("^[6789]\d{9}$",str(customer.phone)) is None:
            return render(request, "user-edit-profile.html", {'wrongphone': True})
        customer.user.save()
        customer.save()
        alert = True
        return render(request, "user-edit-profile.html", {'alert':alert})
    return render(request, "user-edit-profile.html")

@login_required(login_url = '/user_login')
def book_turf(request):
    turf = Turf.objects.all()
    return render(request, "book-turf.html", {'turfs':turf})

@login_required(login_url = '/user_login')
def view_user_turf_details(request, myid):
    t = Turf.objects.get(id=myid)
    return render(request, "view-user-turf-details.html", {'turf':t})


@login_required(login_url = '/user_login')
def check_availability(request, myid):
    if request.method == "POST":
        for_date = request.POST['for_date']
        for_time = request.POST['for_time']
        turf_id = request.POST['id']

        b = Booking.objects.filter(turf_id = turf_id, for_date=for_date, for_time=for_time)
        print(b)
        if not b:
            t = Turf.objects.filter(id=turf_id)
            request.session['for_date'] = for_date
            request.session['for_time'] = for_time
            request.session['turf_id'] = turf_id
            request.session['charges'] = t[0].charges
            return redirect("/payment")
        alert = True
        return render(request, "check-availability.html", {'alert':alert, 'id': turf_id})
    return render(request, "check-availability.html", {'id': myid})

@login_required(login_url = '/user_login')
def payment(request):
    if request.method == "POST":
        book_date = date.today()
        for_date = request.session['for_date']
        for_time = request.session['for_time']
        charges = request.session['charges']
        card_no = request.POST['card_no']
        card_holder = request.POST['card_holder']
        bank_name = request.POST['bank_name']
        customer_id = request.session['cid']
        turf_id = request.session['turf_id']

        b = Booking.objects.create(booking_date = book_date, for_date = for_date, for_time = for_time, charges = charges, card_no = card_no, card_holder = card_holder, bank_name = bank_name, customer_id = customer_id, turf_id = turf_id)
        b.save()
        alert = True
        return render(request, "payment.html", {'alert':alert})
    return render(request, "payment.html")

@login_required(login_url = '/user_login')
def mybookings(request):
    bookings = Booking.objects.select_related('turf').filter(customer_id=request.session['cid'])
    return render(request, "mybookings.html", {'bookings':bookings})

@login_required(login_url = '/user_login')
def view_receipt(request, myid):
    b = Booking.objects.select_related('customer', 'turf').get(id=myid)
    return render(request, "view-receipt.html", {'b':b})

@login_required(login_url = '/user_login')
def post_feedback(request):
    if request.method == "POST":
        customer_id = request.session['cid']
        feedback_message = request.POST['feedback_message']
        f = Feedback.objects.create(feedback_message=feedback_message, customer_id=customer_id)
        f.save()
        alert = True
        return render(request, "post-feedback.html", {'alert':alert})
    return render(request, "post-feedback.html")

@login_required(login_url = '/adminlogin')
def bookings(request):
    bookings = Booking.objects.select_related('customer','turf').filter()
    return render(request, "bookings.html", {'bookings':bookings})

@login_required(login_url = '/adminlogin')
def feedback(request):
    feedbacks = Feedback.objects.select_related('customer').filter()
    return render(request, "feedbacks.html", {'feedbacks':feedbacks})

@login_required(login_url = '/adminlogin')
def view_contacts(request):
    contacts = Contact.objects.all()
    return render(request, "view-contacts.html", {'contacts':contacts})

@login_required(login_url = '/adminlogin')
def report(request):
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        bookings = Booking.objects.select_related('customer','turf').filter(booking_date__range=[from_date, to_date])
        return render(request, "bookings.html", {'bookings':bookings})

    return render(request, "report.html")

def bookturf(request):
    turf = Turf.objects.all()
    return render(request, "bookturf.html", {'turfs':turf})

@login_required(login_url = '/adminlogin')
def delete_contact(request, myid):
    c = Contact.objects.get(id=myid)
    c.delete()
    return redirect("/view_contacts")
