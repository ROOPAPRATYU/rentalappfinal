from .tasks import send_notification,send_email_notification,change_status,send_mail_to_owner
from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from propertyManager.models import PropertyDetail
from django.core.mail import send_mail
from rental_application.settings import EMAIL_HOST_USER
import datetime

def sendnotification(request):
    send_notification.delay()
    return HttpResponse("sent whatsapp message ")
#to perform the periodic task
def schedule_sms(request):
    schedule,created=CrontabSchedule.objects.get_or_create(hour=12,minute=30,day_of_month=3)
    task=PeriodicTask.objects.create(crontab=schedule,name="schedule_message_whatsapp"+"4",task="notification.tasks.send_notification")
    return HttpResponse('done scheduled a task')

def send_email(request):
    send_email_notification.delay()
    return HttpResponse("sent email")

def schedule_mail(request):
    tenentdetails=PropertyDetail.objects.values_list("email","rent_date","rent","phone_number","tenant_name","property_name","bhk","is_paid","rent_token","is_tenant_active","owner","owner__email","owner_rent_token_paid","rent_due_date")
    for user in tenentdetails:
        timing=datetime.datetime.today()
        if user[13]==timing.day:
            schedule,created=CrontabSchedule.objects.get_or_create(hour=00,minute=00,day_of_month=user[13])
            task=PeriodicTask.objects.get_or_create(crontab=schedule,name="schedule_email"+user[0],task="notification.tasks.send_email_notification")
            
    return HttpResponse('done scheduled a task')

def verify_payment_token(request,token):
    try:
        obj=PropertyDetail.objects.get(rent_token=token)
        if obj.is_paid==False:
            obj.is_paid=True
            obj.save()
            send_mail_to_owner.delay(token=obj.rent_token,email=obj.email)
            #send_email_to_owner.delay(token=obj.rent_token)
            return HttpResponse("Thank you for confirming your rent pay and sent email to owner with same confirmation")
        return HttpResponse("already verified with this user payment")
    except Exception as e:
        return HttpResponse("invalid token")

def set_status(request):
    change_status.delay()
    return HttpResponse("changed status for paid rent to not paid")

def schedule_status(request):
    schedule,created=CrontabSchedule.objects.get_or_create(hour=00,minute=00,day_of_month=1)
    task=PeriodicTask.objects.create(crontab=schedule,name="schedule_status"+"1",task="notification.tasks.change_status")
    return HttpResponse("done scheduled a task")
    
def owner_rent_token_paid(request,token):
    obj=PropertyDetail.objects.get(owner_rent_token_paid=token)
    if obj.is_paid==True:
        obj.is_paid=True
        obj.save()
        return HttpResponse ("actually paid and status changed")
    return HttpResponse ("invalid token")
def owner_rent_token_not_paid(request,token):
    obj=PropertyDetail.objects.get(owner_rent_token_paid=token)
    if obj.is_paid==True:
        obj.is_paid=False
        obj.save()
        return HttpResponse ("actually not paid and status changed")
    return HttpResponse ("Invalid token for")