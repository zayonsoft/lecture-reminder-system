from django.shortcuts import redirect
from django.contrib import messages, auth

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("dashboard")
        
    return wrapper_func

def lecturers_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.profile.is_lecturer:
            return view_func(request, *args, **kwargs)
        
        elif request.user.profile.is_student:
            return redirect("dashboard")
        
        elif request.user.profile.is_admin:
            return redirect("admin_home")
        
    return wrapper_func

def student_dashboard(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.profile.is_student:
            return view_func(request, *args, **kwargs)
        
        elif request.user.profile.is_lecturer:
            return redirect("lecturer_dashboard")
        
        elif request.user.profile.is_admin:
            return redirect("admin_home")
        
    return wrapper_func

def no_admins(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not (request.user.is_superuser  or request.user.profile.is_admin ):
            return view_func(request, *args, **kwargs)
        else:
            # auth.logout(request)
            # messages.error(request, "Admins Cannot Access This Page!")
            # return redirect("login")
            
            return redirect('admin_home')
        
    return wrapper_func


def admin_dashboard(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.profile.is_admin:
            return view_func(request, *args, **kwargs)
        
        elif request.user.profile.is_student:
            return redirect("dashboard")
        
        elif request.user.profile.is_lecturer:
            return redirect("lecturer_dashboard")
        
    return wrapper_func