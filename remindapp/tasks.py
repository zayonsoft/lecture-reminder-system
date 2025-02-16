from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime

from django.conf import settings

from remindapp.models import Task, Profile


def sendReminderMail():
    students = Profile.objects.filter(is_student = True)
    for student in students:
        tasks = Task.objects.filter(level = student.level, department = student.department, due_date__date = datetime.today()).order_by("due_date")
        student_email = student.user.email
        recipient_list = [student_email] 
        context={
            "todays_tasks": tasks,
            "current_user":student.user,
            "current_date": datetime.strftime(datetime.now(), "%d - %M -%Y")
        }
        html_content = render_to_string('email_template.html', context)
    
        # Create a plain text version of the HTML email
        text_content = strip_tags(html_content)
    
        # Create the email message
        msg = EmailMultiAlternatives("DAILY LECTURE TASK REMINDER", text_content, settings.EMAIL_HOST_USER, recipient_list)
        msg.attach_alternative(html_content, "text/html")
    
        # try:
        #     if student_email:
        #         msg.send()
        #     return True
        # except:
        #     return False
    
