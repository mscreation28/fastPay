from django.urls import path
from ewalletapp.views import login,auth_view,home,signup,logout_request,email_sent,otpvalidate,recharge,money_transfer,send_money,money_transfer_to_user,profile_detail,update_email,update_personal_detail,update_mobile,update_password,user_profile_pic,home1,aboutus,send_mail_contact
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', login),
    url(r'^login/$', login),
    url(r'^auth/$', auth_view),
    url(r'^home/$', home1),
    url(r'^signup/$', signup),
    url(r'^logout/$', logout_request),
    url(r'^email_sent/$', email_sent),
    url(r'^otpvalidate/$',otpvalidate),
    url(r'^recharge/$',recharge),
    url(r'^money_transfer/$',money_transfer),
    url(r'^money_transfer_to_user/$',money_transfer_to_user),
    url(r'^send_money/$',send_money),
    url(r'^profile_detail/$',profile_detail),
    url(r'^update_email/$',update_email),
    url(r'^update_personal_detail/$',update_personal_detail),
    url(r'^update_mobile/$',update_mobile),
    url(r'^update_password/$',update_password),
    url(r'^user_profile_pic/$',user_profile_pic),
    url(r'^transaction/$',home),
    url(r'^aboutus/$',aboutus),
    url(r'^send_mail_contact/$',send_mail_contact),
]