from django.shortcuts import render,redirect
from django.contrib import messages
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,get_user_model,logout
from django.views.decorators.cache import never_cache
from .models import OTP
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.
@never_cache
def sign_up(request):
    User = get_user_model()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')


        if any(char.isdigit() for char in username):
            messages.error(request, "Username cannot contain digits.")
            return redirect('sign_up')

        if User.objects.filter(username = username).exists():
            messages.error(request,"name already exists")
            return redirect('sign_up')
        
        if User.objects.filter(email = email).exists():
            messages.error(request,"email already exists")
            return redirect('sign_up')
        
        if User.objects.filter(phone_number = phone_number).exists():
            messages.error(request,"phone number already exists")
            return redirect('sign_up')
        
        if password != confirm_password:
            messages.error(request,"password not match.")
            return redirect('sign_up')
        

        myuser = User.objects.create_user(username = username, email = email, phone_number = phone_number, password = password)
        myuser.save()

        return redirect('user_login')
    else:
        return render(request,'sign-up.html')








@never_cache
def user_login (request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        myuser = authenticate(username=username,password=password)
        if myuser is not None:
            otp_instance = OTP.generate_otp(myuser)  # Generate OTP and store it in the database
            send_otp_email(myuser, otp_instance)  # Send OTP to user's email
            request.session['otp_id'] = otp_instance.id  # Store OTP instance ID in session
            return redirect('verify_otp')  # Redirect to OTP verification page
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('user_login')

    else:
        return render(request,'login.html')
    
        





@never_cache
@login_required(login_url='user_login')
def user_logout (request):
    if request.user.is_authenticated :
        logout(request)
    return redirect('user_login')


def admin_login(request):
    admin = 'admin'
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        myuser = authenticate(username=username,password=password)
        if myuser is not None:
            login(request,myuser)
            if myuser.is_staff:
                return redirect('admin_dash')
            else:
                messages.error(request,'invalid credentials')
                return render(request,'login.html',{'admin': admin})
        else:
            messages.error(request,'invalid credentials')
            return render(request,'login.html',{'admin': admin})

    else:
        return render(request,'login.html',{'admin': admin})
    

def send_otp_email(user, otp_instance):
    subject = "Your OTP Code"
    message = f"Your OTP code is {otp_instance.otp}. It expires in 5 minutes."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])



def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_id = request.session.get('otp_id')

        if otp_id:
            otp_instance = OTP.objects.get(id=otp_id)

            if otp_instance.is_expired():
                messages.error(request, "The OTP has expired.")
                return redirect('user_login')

            if otp_instance.otp == otp:
                # OTP matches and is valid
                login(request, otp_instance.user)  # Log the user in
                del request.session['otp_id']  # Remove OTP from session
                return redirect('home')  # Redirect to home or another page
            else:
                messages.error(request, "Invalid OTP.")
                return redirect('verify_otp')
        else:
            return redirect('user_login')  # If OTP ID is not in the session, redirect to login
    return render(request, 'verify_otp.html')