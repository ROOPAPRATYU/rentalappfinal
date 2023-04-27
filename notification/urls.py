from django.urls import path
from. views import sendnotification,schedule_sms,send_email,schedule_mail,verify_payment_token,set_status,schedule_status,owner_rent_token_paid,owner_rent_token_not_paid

urlpatterns = [
    
    path("sendsms/",sendnotification,name="sendnotification"),
    path("scheduletask/",schedule_sms,name="sheduletask"),
    path("schedulemail/",schedule_mail,name="emailschedule"),
    path("sendmail/",send_email,name="sendemail"),
    path("varify/<str:token>",verify_payment_token),
    path("setstatus/",set_status,name="changestatus"),
    path("schedulestatus/",schedule_status,name="schedule_status"),
    path("owner/token/verify/<str:token>",owner_rent_token_paid,name="ownerrenttokenpaid"),
    path("owner/verify/notpaid/rent/<str:token>",owner_rent_token_not_paid,name="notpaid")]