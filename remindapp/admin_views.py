from django.shortcuts import render, redirect
from remindapp.models import Level, Course
from django.contrib import messages

from remindapp.decorators import admin_dashboard, authenticated_user

base_path = 'components/admins'


@authenticated_user
@admin_dashboard
def home(request):
    context={
    "page_name":"ADMIN HOME",
    "active_name":"home",
    }
    return render(request, f'{base_path}/admin_home.html', context)


@authenticated_user
@admin_dashboard
def level(request):
    levels = Level.objects.all()
    context={'levels':levels}
    return render(request, f'{base_path}/levels/levels.html', context)


@authenticated_user
@admin_dashboard
def addLevel(request):
    previous_name = ''
    if request.method == "POST":
        name = request.POST.get('name')
        if not (name and name.strip()):
            messages.error(request, "Name Cannot Be Empty..")
            return redirect("add_level")
        
        name = name.strip()
        previous_name = name 
        
        if Level.objects.filter(name__iexact = name ).exists():
            messages.error(request, "Level Already Exists")
            return redirect("add_level")
        
        Level.objects.create(name = name)
        messages.success(request, 'Level Added Successfully')
        return redirect("levels")
    
    context = {"previous_name": previous_name}
    
    return render(request, f'{base_path}/levels/add_level.html', context)


@authenticated_user
@admin_dashboard
def editLevel(request, pk):
    if not pk.isdigit():
        messages.error(request, "Something Went Wrong!")
        return redirect("levels")
    
    if not Level.objects.filter(id = pk).exists():
        messages.error(request, "Data Not Found!")
        return redirect("levels")
    
    level = Level.objects.get(id = pk)
    context={"level":level}
    
    if request.method == "POST":
        name = request.POST.get('name')
        if not (name and name.strip()):
            messages.error(request, "Name Cannot Be Empty..")
            return redirect("edit_level",level.id)
        
        name = name.strip()
        
        if level.name.upper() == name.upper():
            messages.error(request, "Unchanged Data")
            return redirect("edit_level",level.id)
        
        if Level.objects.filter(name__iexact = name ).exists():
            messages.error(request, f"'{name}' Already Exists!")
            return redirect("edit_level",level.id)
        
        level.name = name
        level.save()
        messages.success(request, 'Data Updated Successfully')
        return redirect("levels")
        
    return render(request, f'{base_path}/levels/edit_level.html', context)


@authenticated_user
@admin_dashboard
def deleteLevel(request, pk):
    if not request.method == "POST":
        messages.error(request, "Method Disallowed!")
        
    if not pk.isdigit():
        messages.error(request, "Something Went Wrong!")
        return redirect("levels")
    
    if not Level.objects.filter(id = pk).exists():
        messages.error(request, "Data Not Found!")
        return redirect("levels")
    
    level = Level.objects.get(id = pk)
    level.delete()
    messages.success(request, "Deleted Successfully")
    return redirect("levels")

            
@authenticated_user
@admin_dashboard
def courses(request):
    courses = Course.objects.all()
    context={'courses':courses}
    return render(request, f'{base_path}/courses/courses.html', context)
    