from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .forms import RequestForm
from .models import smtp # type: ignore

# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        
        if password != cpassword:
            messages.error(request, "Passwords do not match. Please retry.")
            return redirect("/signup")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("/signup")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("/signup")
        
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.save()       
        return redirect("/login")
    
    else:
        messages.info(request, "Please sign up.")
        
    return render(request, "signup.html")

def hendel_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        myuser = authenticate(username=username, password=password)
        
        if myuser is not None:
            login(request, myuser)
            if myuser.is_superuser:  # Check if the user is an admin
                messages.success(request, 'Admin login successful')
                return redirect('admin_panel')  # Redirect to admin panel
            else:
                messages.success(request, 'User login successful')
                return redirect('request_form')  # Redirect to request form
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
        
    return render(request, "login.html")

@login_required(login_url="/login")
def admin_panel(request):
    pending_requests = smtp.objects.all()
    context = {'pending_requests': pending_requests}
    return render(request, 'admin_panel.html', context)

@login_required(login_url="/login")
def approv(request, req_id):
    req = smtp.objects.get(pk=req_id)
    subject = 'Request Approved'
    context = {'request': req}
    html_message = render_to_string('approv.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'chendu167@gmail.com'
    recipient_list = [req.Email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return HttpResponse('Request approved and email sent successfully!')

@login_required(login_url="/login")
def rejected(request, req_id):
    req = smtp.objects.get(pk=req_id)
    subject = 'Request Rejected'
    context = {'request': req}
    html_message = render_to_string('rejected.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'chendu167@gmail.com'
    recipient_list = [req.Email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return HttpResponse('Request rejected and email sent successfully!')

@login_required
def new_request(request):
    if request.method == 'POST':
        subject = 'New Request Submitted'
        message = 'A new request has been submitted. Please log in to the admin panel to review it.'
        
        # Assuming the user's email is stored in the User model's email field
        from_email = request.user.email
        
        recipient_list = ['chendu167@gmail.com']  # Replace with admin's email
        
        # Use send_mail from django.core.mail
        send_mail(subject, message, from_email, recipient_list)
        
        # Additional logic if needed, e.g., return a response or redirect
        return HttpResponse("Email sent successfully")
    else:
        # Handle GET request or other methods if needed
        return HttpResponse("Invalid request method")

@login_required(login_url="/login")
def request_form(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            # Send email notification to admin
            new_request(request)
            messages.success(request, 'Request submitted successfully.')
            return redirect('login')
    else:
        form = RequestForm()
    return render(request, 'request.html', {'form': form})

def base(request):
    return render(request, "base.html")

def send_verification_email(user):
    subject = 'Verify your email address'
    message = 'Please click the link below to verify your email address.'
    from_email = 'abc@gmail.com'
    to_email = user.email
    send_mail(subject, message, from_email, [to_email])
