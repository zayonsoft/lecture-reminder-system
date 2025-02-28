from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from remindapp.year_developed import year_developed

from django.conf import settings

def sendTaskMail(task, message_header):
    context={}
    profiles = task.level.profile_set.all()
    sent = 0
    not_sent = 0
    
    for student in profiles:
        student_email = student.user.email
        recipient_list = [student_email]
        context={
            "task":task,
            "message_header":message_header,
            "current_user":student.user,
            "current_date": datetime.strftime(datetime.now(), "%d - %m -%Y"),
            "user": student.user,
            "created_by":task.user,
            "year_developed": year_developed ,
            "current_year": datetime.now().year ,
        }
        html_content = render_to_string('task_info_mail.html', context)
    
        # Create a plain text version of the HTML email
        text_content = strip_tags(html_content)
    
        # Create the email message
        msg = EmailMultiAlternatives("TASK NOTIFICATION", text_content, settings.EMAIL_HOST_USER, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        
        try:
            if student_email:
                msg.send()
                sent +=1
        except:
            not_sent +=1
            
            
    #for the creator
    context["user"] = task.user
    html_content = render_to_string('task_info_mail.html', context)
    
    msg2 = EmailMultiAlternatives("TASK NOTIFICATION", text_content, settings.EMAIL_HOST_USER, [task.user.email])
    msg2.attach_alternative(html_content, "text/html")
    try:
    # if 1:
        msg2.send()
        print("Task Owner Mail Successfully Sent")
    except:
    # else:
        print("Couldn't Send Mail to Creator")
    
        
    print(f"{sent} Student Mail(s) Sent, {not_sent} Unsent!!")