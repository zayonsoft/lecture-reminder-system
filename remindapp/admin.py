from django.contrib import admin
from remindapp.models import Level, Department, Profile, TaskType, Course
# Register your models here.


admin.site.register(Level)
admin.site.register(Department)
admin.site.register(Profile)
admin.site.register(TaskType)
admin.site.register(Course)