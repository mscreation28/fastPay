from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from ewalletapp.forms import UserRegisterForm,ProfileForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.views.generic import ListView
from ewalletapp.models import Jio,Vodafone,Transaction, Profile
import random

def login(request):
    c = {}
    c.update(csrf(request))
    # print("tetst msg for login")
    return render(request,'login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    request.session['password']=password
    # print("tetst msg for auth")
    user = auth.authenticate(username=username,password=password)
    if user is not None:
        # print("inside if for auth tetst msg")
        auth.login(request, user)
        return HttpResponseRedirect('/home')
    else:
        messages.add_message(request,messages.WARNING,'Invalid Login Details')
        return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        
        if form.is_valid():     
            request.session['email_add']=form.cleaned_data.get('email')
            request.session['username']=form.cleaned_data.get('username')
            request.session['fname']=form.cleaned_data.get('first_name')
            request.session['lname']=form.cleaned_data.get('last_name')
            request.session['pwd']=form.cleaned_data.get('password1')

            return redirect('/email_sent')
    else:
        form=UserRegisterForm()
    return render(request,'signup.html',{'form':form})


@login_required(login_url='/login')
def home(request):
    request.session['username']=request.user.username
    u = User.objects.get(username = request.session['username'])
    
    ans= Transaction.objects.filter(receiver=request.session['username']) | Transaction.objects.filter(user=u)
    
    paginator = Paginator(ans, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'transaction.html',{'page_obj': page_obj})


def logout_request(request):
    logout(request)
    return redirect('/login')

def email_sent(request):
    subject = 'Thank you for registering to our site'
    email_from = settings.EMAIL_HOST_USER
    otp = random.randint(100000,999999)
    request.session['otp']=otp
    print(otp)
    resp_list=[]
    resp_list.append(request.session['email_add'])
    send_mail( subject, str(otp), email_from, resp_list )
    return render(request,'email_sent.html')

def otpvalidate(request):
    otp1=request.session['otp']
    print(otp1)
    otp2=request.POST['otp']
    print(otp2)
    
    if(str(otp1)==otp2):
        print("yes")
        user=User.objects.create_user(username=request.session['username'],email=request.session['email_add'],first_name=request.session['fname'],last_name=request.session['lname'],password=request.session['pwd'])

        user.refresh_from_db() 
        user.profile.amount=1000
        user.profile.debit=0
        user.profile.credit=1000
        user.profile.save()
        recieve="mscreation"
        r = User.objects.get(username = recieve)
        r.profile.amount-=1000
        r.profile.debit+=1000
        r.profile.save()
        trans=Transaction()
        trans.user=r
        trans.amount=1000
        trans.t_type="Money Transfer"
        trans.receiver=request.session['username']
        trans.save()

        messages.add_message(request,messages.SUCCESS, 'Profile details updated.')
        return render(request,'login.html')
    else:    
        messages.warning(request, 'Invalid OTP, Try Again!')
        return render(request,'email_sent.html')


def recharge(request):
    return render(request,'recharge.html')

def money_transfer(request):
    print(request.session['username'])
    username=request.session['username']
    u = User.objects.get(username = username)
    # print(u.profile.amount)
    amount=int(request.POST['plan'])
    
    if(u.profile.amount>=amount):
        u.profile.amount-=amount
        u.profile.debit+=amount
        u.profile.save()
        trans=Transaction()
        trans.user=u
        trans.amount=amount
        trans.t_type="Recharge"
        trans.receiver=(request.POST['mb_number'])
        trans.save()

        if(request.POST['operator']=='jio'):
            opr=Jio()
            opr.amount=amount
            opr.mobile_number=request.POST['mb_number']
            opr.state=request.POST['circle']
            opr.save()
        elif(request.POST['operator']=='vodafone'):
            opr=Vodafone()
            opr.amount=amount
            opr.mobile_number=request.POST['mb_number']
            opr.state=request.POST['circle']
            opr.save()
        messages.add_message(request,messages.SUCCESS,'Recharged Successfully')
        return render(request,'recharge.html')
    else:
        messages.add_message(request,messages.WARNING,'Insufficient Amount!')
        return render(request,'recharge.html')

def send_money(request):
    return render(request,'send_money.html')

def money_transfer_to_user(request):
    print(request.session['username'])
    username=request.session['username']
    u = User.objects.get(username = username)
    r = User.objects.get(username = request.POST['rname'])
    amount=int(request.POST['amount'])
    if(u.profile.amount>=amount):
        u.profile.amount-=amount
        u.profile.debit+=amount
        u.profile.save()
        r.profile.amount+=amount
        r.profile.credit+=amount
        r.profile.save()
        trans=Transaction()
        trans.user=u
        trans.amount=amount
        trans.t_type="Money Transfer"
        trans.receiver=(request.POST['rname'])
        trans.save()
        messages.add_message(request,messages.SUCCESS,'Money Transfered Successfully')
        return render(request,'send_money.html')
    else:
        messages.add_message(request,messages.WARNING,'Insufficient Amount!')
        return render(request,'send_money.html')


def profile_detail(request):
    return render(request,'profile_detail.html')

def update_email(request):
    username=request.session['username']
    u = User.objects.get(username = username)
    u.email=request.POST['umail']
    u.save()
    return render(request,'profile_detail.html')
    
def update_personal_detail(request):
    username=request.session['username']
    u = User.objects.get(username = username)
    u.first_name=request.POST['ufname']
    u.last_name=request.POST['ulname']
    u.profile.birth_date=request.POST['udate']
    u.save()
    u.profile.save()
    return render(request,'profile_detail.html')

def update_mobile(request):
    username=request.session['username']
    u = User.objects.get(username = username)
    u.profile.mobile_number=request.POST['umobile']
    u.profile.save()
    return render(request,'profile_detail.html')

def update_password(request):
    username=request.session['username']
    u = User.objects.get(username = username)
    username = request.session['username']
    password = request.POST['upwd']
    u.set_password(request.POST['upwd'])
    u.save()
    user = auth.authenticate(username=username,password=password)
    
    if user is not None:
        # print("inside if for auth tetst msg")
        auth.login(request, user)
        return HttpResponseRedirect('/profile_detail')
    return render(request,'profile_detail.html')

def user_profile_pic(request):
    username=request.session['username']
    u = User.objects.get(username = username)

    if request.method == "POST":
        MyProfileForm = ProfileForm(request.POST,request.FILES)   
        
        if MyProfileForm.is_valid():          
            u.profile.profile_pic = MyProfileForm.cleaned_data["picture"]
            u.profile.save()

    return render(request,'profile_detail.html')

@login_required(login_url='/login')
def home1(request):
    return render(request,'home.html')

def aboutus(request):
    return render(request,'aboutus.html')

def send_mail_contact(request):
    subject = request.POST['sub']
    msg=request.POST['msg']
    email_from = settings.EMAIL_HOST_USER
    resp_list=[]
    resp_list.append("makwanashyam28@gmail.com")
    send_mail( subject, msg, email_from, resp_list )
    return render(request,'aboutus.html')

