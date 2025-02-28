from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime

from django.conf import settings
from decouple import config

from remindapp.models import Task, Profile

class Command(BaseCommand):
    help = "Send daily task reminder emails to users."
    
    def handle(self, *args, **kwargs):
        profiles = Profile.objects.filter(is_student = True)
        sent = 0
        not_sent = 0
        for student in profiles:
            lecturer_tasks = Task.objects.filter(level = student.level, department = student.department, due_date__date = datetime.today()).order_by("due_date")
            student_email = student.user.email
            recipient_list = [student_email]
            context={
                "todays_tasks": lecturer_tasks,
                "current_user":student.user,
                "current_date": datetime.strftime(datetime.now(), "%d - %m -%Y"),
                "user": student.user,
                "host_url":config('HOST_URL', default=""),
            }
            html_content = render_to_string('email_template.html', context)
        
            # Create a plain text version of the HTML email
            text_content = strip_tags(html_content)
        
            # Create the email message
            msg = EmailMultiAlternatives("DAILY LECTURE TASK REMINDER", text_content, settings.EMAIL_HOST_USER, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            
            try:
                if student_email:
                    msg.send()
                    sent +=1
            except:
                not_sent +=1
                
                
        #SENDING A REMNDER FOR TASKS EXPIRING FOR THE LECTURER
        
        lecturers = Profile.objects.filter(is_lecturer = True)            
        lecturer_sent = 0
        lecturer_not_sent = 0
        
        for lecturer in lecturers:
            lecturer_tasks = Task.objects.filter(user = lecturer.user, due_date__date = datetime.today()).order_by("due_date")
            
            lecturer_email = lecturer.user.email
            recipient_list = [lecturer_email]
            context={
                "todays_tasks": lecturer_tasks,
                "current_user":lecturer.user,
                "current_date": datetime.strftime(datetime.now(), "%d - %m -%Y"),
                "user": lecturer.user,
                "host_url":config('HOST_URL', default=""),
            }
            html_content = render_to_string('email_template.html', context)
        
            # Create a plain text version of the HTML email
            text_content = strip_tags(html_content)
        
            # Create the email message
            lecturer_msg = EmailMultiAlternatives("DAILY LECTURE TASK REMINDER", text_content, settings.EMAIL_HOST_USER, recipient_list)
            lecturer_msg.attach_alternative(html_content, "text/html")
            try:
                lecturer_msg.send()
                lecturer_sent +=1
            except:
                lecturer_not_sent +=1
            
            
        self.stdout.write(self.style.SUCCESS(f"{sent} Mail(s) Sent, {not_sent} Unsent!!"))
        self.stdout.write(self.style.SUCCESS(f"{lecturer_sent} Lecturer Mail(s) Sent, {lecturer_not_sent} Unsent!!"))