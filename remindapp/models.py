from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import UniqueConstraint


# Create your models here.

class Level(models.Model):
    name = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.name
    

class Department(models.Model):
    name = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null=True)
    profile_id = models.CharField(max_length=60, blank=True, null=True, unique = True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, blank = True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    is_lecturer = models.BooleanField(default = False)
    is_student = models.BooleanField(default = False)
    is_admin = models.BooleanField(default=False)
    is_updated = models.BooleanField(default = False)
    
    def clean(self):
        if sum([self.is_student, self.is_lecturer, self.is_admin]) != 1:
            raise ValidationError("User Can only be one of admin, student or lecturer")
        
    def __str__(self):
        if self.is_lecturer:
            return f"{self.profile_id} - Lecturer"
        
        if self.is_student:
            return f"{self.profile_id} - Student"
        
        if self.is_admin:
            return f"{self.profile_id} - Admin"
        
        
                

# for instance test, presentation Lecture e.t.c
class TaskType(models.Model):
    name = models.CharField(max_length = 500)
    
    def __str__(self):
        return self.name
    
    
class Course(models.Model):
    course_code = models.CharField(max_length=55)
    course_title = models.TextField(default="-")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.course_code


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to="task_files/", blank=True, null=True)
    description = models.TextField(default="")
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateField(auto_now_add = True)
    due_date = models.DateTimeField(null = True, blank = True)
    allow_reply = models.BooleanField(default = True)
    allow_files = models.BooleanField(default = False)
    allow_edit_response = models.BooleanField(default = False)
    last_modified = models.DateTimeField(blank = True, null= True)
    
    def save(self, *args, **kwargs):
        self.last_modified = datetime.now()
        super().save(*args, **kwargs)
    
class TaskReply(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to="task_reples/", blank=True, null=True)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(blank = True, null= True)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['student', 'task'], name='unique_student_task')
        ]
        
        
    def save(self, *args, **kwargs):
        self.last_modified = datetime.now()
        super().save(*args, **kwargs)