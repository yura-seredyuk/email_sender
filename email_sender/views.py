from django.shortcuts import render, get_object_or_404
from django.conf import settings
import pandas as pd

from django.core.mail import EmailMessage


def homepage(request):
    if request.method == 'POST':
        SHEET_URL = request.POST['sheet_url']
        URL_EDITED = SHEET_URL.replace("/edit#gid=", "/export?format=csv&gid=")
        data = pd.read_csv(URL_EDITED)  
        for email in data['email']:
            email = email.replace(' ','')
            print(email)

            subject = f'Subject: {request.POST.get("subject")}'
            body = f'Message:\n{request.POST["message"]}'
            email = EmailMessage(subject, body, to=[email])
            email.send()

    return render(request, 'index.html')