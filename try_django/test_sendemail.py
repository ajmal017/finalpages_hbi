from django.core.mail import send_mail
from django.http import HttpResponse

def sending_mail(request):
    #send_mail('Example Subject-10:32am', 'Example message-10:32am', 'smilingideas@gmail.com', ['tangpd@hotmail.com','heydudde@gmail.com'])
    send_mail('Hello There! Subject-5:52pm Date 21/5/2020', 'Hello There! message-5:52pm', 'smilingideas@gmail.com',['tangpd@hotmail.com', 'heydudde@gmail.com'])
    return HttpResponse('email sent at 5:52pm Date 21/5/2020!')