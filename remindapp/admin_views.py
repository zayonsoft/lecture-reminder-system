from django.shortcuts import render, redirect
from remindapp.models import Level, Course
from django.contrib import messages

base_path = 'components/admins'

def home(request):
    context={
    "page_name":"ADMIN HOME",
    "active_name":"home",
    }
    return render(request, f'{base_path}/admin_home.html', context)

def level(request):
    levels = Level.objects.all()
    context={'levels':levels}
    return render(request, f'{base_path}/levels/levels.html', context)


def addLevel(request):
    previous_name = ''
    if request.method == "POST":
        name = request.POST.get('name')
        if not name and name.strip():
            messages.error(request, "Level Already Exists")
            return redirect("add_level")
        
        name = name.strip()
        previous_name = name 
        
        if not Level.objects.filter(name__iexact = name ).exists():
            messages.error(request, "Level Already Exists")
            return redirect("add_level")
    
    context = {"previous_name": previous_name}
    
    return render(request, f'{base_path}/levels/add_level.html', context)
    
            

def courses(request):
    courses = Course.objects.all()
    context={'courses':courses}
    return render(request, f'{base_path}/courses/courses.html', context)
    