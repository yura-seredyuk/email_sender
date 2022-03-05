from django.shortcuts import render, get_object_or_404
from django.conf import settings
import pandas as pd
import urllib
import smtplib
from django.core.mail import EmailMessage
from django.contrib import messages


def homepage(request):
    if request.method == 'POST':
        try:
            SHEET_URL = request.POST['sheet_url']
            URL_EDITED = SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid=")
            data = pd.read_csv(URL_EDITED)
            sender_email = request.POST['email']  
            sender_password = request.POST['password']
            if sender_email != '' and sender_password != '':
                settings.EMAIL_HOST_USER = sender_email
                settings.EMAIL_HOST_PASSWORD = sender_password                
            for email in data['email']:
                email = email.replace(' ','')
                print(email)
                subject = f'Subject: {request.POST.get("subject")}'
                body = f'Message:\n{request.POST["message"]}'
                email = EmailMessage(subject, body, to=[email])
                email.send()
            messages.info(request, 'All messages was sended!')
        except Exception as e:
            if isinstance(e, KeyError):
                messages.error(request, f'Incorrect file structure. Missed "email" title in cell A1! Message: {e}')
            elif isinstance(e, (urllib.error.HTTPError,)):
                messages.error(request, f'Wrong-site URL. Must be the "docs.google.com/spreadsheets" table link! Message: {e}')
            elif isinstance(e, (pd.errors.ParserError,FileNotFoundError)):
                messages.error(request, f'Incorrect site URL. Copy link from the URL address field in your web browser! Message: {e}')
            elif isinstance(e, (smtplib.SMTPAuthenticationError)):
                messages.error(request, f'Incorrect email settings (incorrect password, wrong or unconfigured email)! Message: {e}')
            else:
                messages.error(request, 'Error. Something was wrong!')
            print(type(e))

    return render(request, 'index.html')