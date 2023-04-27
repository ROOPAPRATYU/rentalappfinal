from celery import shared_task
from twilio.rest import Client
import datetime
from rental_application.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from django.core.mail import send_mail
from rental_application.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from user_profile.models import OwnerProfile
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from  accounts.models import User
import requests
import json

from propertyManager.models import PropertyDetail
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)   
#to send due notification via
@shared_task(bind=True)
def send_notification(request):
    #collect ("email","rent_date","rent","phone_number") data from the propertydetails database table
    tenentdetails=PropertyDetail.objects.values_list("email","rent_date","rent","phone_number","tenant_name","property_name","bhk")
    for userinfo in tenentdetails:
        timing=datetime.datetime.today()
        message = client.messages.create(from_='whatsapp:+14155238886',body='Hi {} please pay your rent amount {} for property {}({}BHK) ,your rent on due please pay before {}/{}/{},if already paid please ignore it'.format(userinfo[4],userinfo[2],userinfo[5],userinfo[6],timing.day,timing.month,timing.year),to='whatsapp:+91{}'.format(8880869502))
            
    return ('Great! Expect a message on whatsapp..')
#to perform the email due notification via send_email
@shared_task(bind=True)
def send_email_notification(request):
    
    tenentdetails=PropertyDetail.objects.values_list("email","rent_date","rent","phone_number","tenant_name","property_name","bhk","is_paid","rent_token","is_tenant_active","owner","owner__email")
    
    for userinfo in tenentdetails:
        #get owner email id
        obj=OwnerProfile.objects.filter(user_id=userinfo[10])
        owner2=(obj.values_list("first_name"))
        timing=datetime.datetime.today()
        month=timing.month
        year=timing.year
        if userinfo[0] is not None and userinfo[7]==False and userinfo[9]==True:
            #curent_site=get_current_site(request)
            subject = "Property {} Rent Remeinder".format(userinfo[5])
            
            msg=render_to_string("duenotification.html",{
                "tenant_name":userinfo[4],
                "property_name":userinfo[5],
                "bhk":userinfo[6],
                "rent_amount":userinfo[2],
                "living":userinfo[1],
                "rent_token":userinfo[8],
                "month":month,
                "year":year,
                "owner":owner2,
                "owner_mail":userinfo[11]
                #"owner_detals":userinfo[10].email


                #"domain":curent_site
            })
            to =  userinfo[0] 
            text_content=strip_tags(msg)
            email=EmailMultiAlternatives(
                subject,
                text_content,
                EMAIL_HOST_USER,
                [to]
            )
            email.attach_alternative(msg,"text/html")
            email.send()
            
            #send_mail(subject,text_content,EMAIL_HOST_USER, [to])
            
    return ("great expect a email on tenant email")
#to change the is_paid value everymonth
@shared_task(bind=True)
def change_status(request):
    tenentdetails=PropertyDetail.objects.values_list("is_tenant_active","is_paid")
    try:
        obj=PropertyDetail.objects.get(is_paid=True)
        for userinfo in tenentdetails:
            if userinfo[0]==True and userinfo[1]==True:
                obj.is_paid=False
                obj.save()
        return ("changed the status for is_paid rent")
    except:
        return ("no change in status")
@shared_task(bind=True)
def send_mail_to_owner(request,token,email):
    tenentdetails=PropertyDetail.objects.values_list("email","rent_date","rent","phone_number","tenant_name","property_name","bhk","is_paid","rent_token","is_tenant_active","owner","owner__email","owner_rent_token_paid")
    for userinfo in tenentdetails:
        #get owner email id
        obj=OwnerProfile.objects.filter(user_id=userinfo[10])
        owner2=obj.values_list("first_name","last_name")
        timing=datetime.datetime.today()
        month=timing.month
        year=timing.year
        if userinfo[0]==email and token==userinfo[8]:
            #curent_site=get_current_site(request)
            subject = "Property {} Rent Paid".format(userinfo[5])
            
            msg=render_to_string("notify_owner.html",{
                "tenant_name":userinfo[4],
                "property_name":userinfo[5],
                "rent_amount":userinfo[2],
                "month":month,
                "year":year,     
                "owner":owner2[0],
                "phone_number":userinfo[3],
                "owner_rent_token_paid":userinfo[12]
        
            })
            to =  userinfo[11]
            text_content=strip_tags(msg)
            email=EmailMultiAlternatives(
                subject,
                text_content,
                EMAIL_HOST_USER,
                [to]
            )
            email.attach_alternative(msg,"text/html")
            email.send()
            
    return ("great expect a email on owner")