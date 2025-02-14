from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime

from django.conf import settings

from remindapp.models import Task 


def sendMailMessage(reseter, sender_email):
    context={
        "current_date":datetime.now(),
        "reseter":reseter,
    }
    html_content = render_to_string('email_template.html', context)
    
    # Create a plain text version of the HTML email
    text_content = strip_tags(html_content)
    
    # Create the email message
    recipient_list = [reseter.email]
    msg = EmailMultiAlternatives("CGPA CALCULATOR RESET PASSWORD", text_content, sender_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    

    try:
        msg.send()
        return True
    except:
        return False
    
