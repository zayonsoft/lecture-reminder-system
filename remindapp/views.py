from django.shortcuts import render, redirect
from django.contrib import auth, messages
from remindapp.decorators import authenticated_user, unauthenticated_user, no_admins, student_dashboard,lecturers_only
from remindapp.models import Level, Course, Department, TaskReply, Task, TaskType
from datetime import datetime
from django.utils import timezone
from django.urls import reverse


from django.contrib.auth.models import User

# Create your views here.


def errorPage(request, message):
    context = {"message":message}
    return render(request,"errors/errors.html", context)

@unauthenticated_user
def login(request):
    if request.method == "POST":
        user_or_email = request.POST.get("username")
        password = request.POST.get("password")
        
        if not ( User.objects.filter(username = user_or_email).exists() or User.objects.filter(email = user_or_email).exists() ):
            messages.error(request, "Invalid Login Credentials")
            return redirect("login")
        if User.objects.filter(username = user_or_email).exists():
            user = auth.authenticate(username = user_or_email, password = password)
            if user is not None:
                auth.login(request, user)
                # messages.success(request, "Login Successful!")
                return redirect("dashboard")
            else:
                messages.error(request, "Incorrect Password!")
                return redirect("login")
        
        if User.objects.filter(email = user_or_email).exists():
            username = User.objects.get(email = user_or_email).username
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                auth.login(request, user)
                # messages.success(request, "Login Successful!")
                return redirect("dashboard")
            else:
                messages.error(request, "Incorrect Password!")
                return redirect("login")
            
                
    return render(request, "auth/login.html")

def logout(request):
    auth.logout(request)
    return redirect("login")


@authenticated_user
@no_admins
@student_dashboard
def home(request):
    student = request.user.profile
    tasks = Task.objects.filter(level = student.level, department = student.department, due_date__date = datetime.today()).order_by("due_date")
    context={
        "page_name":"HOME",
        "active_name":"home",
        "tasks":tasks,
        "today_date":datetime.today().date,
    }
    return render(request, "components/home.html", context)


@authenticated_user
@no_admins
@lecturers_only
def lecturerHome(request):
    tasks = Task.objects.filter(user = request.user, due_date__date = datetime.today()).order_by("due_date")
    
    context = {
        "page_name":"HOME",
        "active_name":"home",
        "tasks":tasks,
        "today_date":datetime.today().date,
    }
    return render(request,"components/lecturer_home.html", context)
    


@authenticated_user
def viewTasks(request, pk):
    if not pk.isdigit():
        return errorPage(request, "Invalid Task!")
    
    if not Task.objects.filter(id = pk).exists():
        return errorPage(request, "A Corresponding task Doesn't exist!")
    
    task = Task.objects.get(id = pk)
    
    context = {
        "task":task,
        "page_name":"MY TASKS",
        "active_name":"my_tasks",
        }
    return render(request, "components/view_task.html", context)


@authenticated_user
@no_admins
@lecturers_only
def myTasks(request):
    tasks = Task.objects.filter(user = request.user).order_by("due_date")
    
    context={
        "tasks":tasks,
        "page_name":"MY TASKS",
        "active_name":"my_tasks",
        }
    return render(request, "components/my_tasks.html", context)


@authenticated_user
@no_admins
@lecturers_only
def addTask(request):
    current_profile = request.user.profile
    levels = Level.objects.all()
    task_types = TaskType.objects.all()
    dept_courses = Course.objects.filter(department = current_profile.department)
    department = current_profile.department
    
    if request.method == "POST":
        description = request.POST.get("description")
        file = request.FILES.get("attach-file")
        level_id = request.POST.get("level")
        type_id = request.POST.get("task-type")
        course_id = request.POST.get("course")
        deadline = request.POST.get("due-date")
        allow_reply = request.POST.get("allow_reply")
        allow_files = request.POST.get("allow_files")
        allow_editing = request.POST.get("allow_edit")
        
        reply = None
        if allow_reply == "1":
            reply = True
        else:
            reply = False
        
        
        file_allowance = None
        if allow_files == "1":
            file_allowance = True
        else:
            file_allowance =  False
        
        
        edit_allowance = None
        if allow_editing == "1":
            edit_allowance = True
        else:
            edit_allowance =  False
        
        
        
        
        errors = False
        if not description.strip():
            messages.error(request, "A Description Must Be Given")
            errors = True
        
        if not level_id.strip():
            messages.error(request, "Level Not Selected")
            errors = True
        
        if not type_id.strip():
            messages.error(request, "Task Type Not Selected")
            errors = True
        
        if not course_id.strip():
            messages.error(request, "Select A course")
            errors = True
        
        if not Level.objects.filter(id = level_id).exists():
            messages.error(request, "Selected Level Doesnot Exist")
            errors = True
        
        if not Course.objects.filter(id = course_id).exists():
            messages.error(request, "Selected Course Doesnot Exist")
            errors = True
            
        if not TaskType.objects.filter(id = type_id).exists():
            messages.error(request, "Task Type is Invalid")
            errors = True
            
        if errors:
            return redirect("add_task")
        
        if not file:
            file = None 
    
        level =  Level.objects.get(id = level_id)
        course = Course.objects.get(id = course_id)
        task_type = TaskType.objects.get(id = type_id)
        
        formated_deadline = deadline.replace("T", " ")
        
        deadline_date = datetime.strptime(formated_deadline, "%Y-%m-%d %H:%M")
        
        if datetime.now() > deadline_date:
            messages.error(request, "Select a Future Time")
            return redirect("add_task") 
        
        
        Task.objects.create(
            user = request.user,
            level = level,
            course = course,
            department = department,
            attachment = file,
            description = description,
            task_type = task_type,
            allow_reply = reply,
            allow_files = file_allowance,
            allow_edit_response = edit_allowance,
            due_date  = deadline_date,
        )
        
        messages.success(request, "Task Added Successfully!")
        return redirect("my_tasks")
        
    
    context={
        "levels":levels,
        "task_types": task_types,
        "dept_courses": dept_courses,
    }
    return render(request, "components/add_task.html", context) 


@authenticated_user
@no_admins
@lecturers_only
def editTask(request, pk):
    current_profile = request.user.profile
    levels = Level.objects.all()
    task_types = TaskType.objects.all()
    dept_courses = Course.objects.filter(department = current_profile.department)
    department = current_profile.department
    
    if not pk.isdigit():
        return errorPage(request, "Invalid Task!")
    
    if not Task.objects.filter(user = request.user, id = pk).exists():
        return errorPage(request, "A Corresponding task Doesn't exist!")
    
    task = Task.objects.get(user = request.user, id = pk)
    
    task_date = datetime.strftime(task.due_date, "%Y-%m-%dT%H:%M")
    
    context = {"task":task, "levels":levels, "dept_courses":dept_courses, "task_types":task_types, "department":department, "task_date":task_date}
    
    if request.method == "POST":
        description = request.POST.get("description")
        file = request.FILES.get("attach-file")
        level_id = request.POST.get("level")
        type_id = request.POST.get("task-type")
        course_id = request.POST.get("course")
        deadline = request.POST.get("due-date")
        allow_reply = request.POST.get("allow_reply")
        allow_files = request.POST.get("allow_files")
        allow_editing = request.POST.get("allow_edit")
        
        reply = None
        if allow_reply == "1":
            reply = True
        else:
            reply = False
            
        file_allowance = None
        if allow_files == "1":
            file_allowance = True
        else:
            file_allowance =  False
            
        
        edit_allowance = None
        if allow_editing == "1":
            edit_allowance = True
        else:
            edit_allowance =  False
        
        errors = False
        if not description.strip():
            messages.error(request, "A Description Must Be Given")
            errors = True
        
        if not level_id.strip():
            messages.error(request, "Level Not Selected")
            errors = True
        
        if not type_id.strip():
            messages.error(request, "Task Type Not Selected")
            errors = True
        
        if not course_id.strip():
            messages.error(request, "Select A course")
            errors = True
        
        if not Level.objects.filter(id = level_id).exists():
            messages.error(request, "Selected Level Doesnot Exist")
            errors = True
        
        if not Course.objects.filter(id = course_id).exists():
            messages.error(request, "Selected Course Doesnot Exist")
            errors = True
            
        if not TaskType.objects.filter(id = type_id).exists():
            messages.error(request, "Task Type is Invalid")
            errors = True
            
        if errors:
            return redirect("edit_task", task.id)
        
        if not file:
            file = None 
    
        level =  Level.objects.get(id = level_id)
        course = Course.objects.get(id = course_id)
        task_type = TaskType.objects.get(id = type_id)
        
        formated_deadline = deadline.replace("T", " ")
        
        deadline_date = datetime.strptime(formated_deadline, "%Y-%m-%d %H:%M")
        
        if datetime.now() > deadline_date:
            messages.error(request, "Select a Future Time")
            return redirect("edit_task", task.id)
        
        task.level = level
        task.course = course
        
        if file:
            if task.attachment:
                current_file = task.attachment
                if hasattr(current_file, 'close'):
                    current_file.close()
                current_file.delete()
                    
            task.attachment = file
            
        task.description = description
        task.task_type = task_type
        task.allow_reply = reply
        task.allow_files = file_allowance
        task.due_date = deadline_date
        task.allow_edit_response = edit_allowance
        
        task.save()
        messages.success(request, "Successfully Updated Task")
        return redirect("my_tasks") 
    
    
    return render(request, "components/edit_task.html", context)


@authenticated_user
@no_admins
@lecturers_only
def deleteTask(request, task_id):
        
    if not task_id.isdigit():
        return errorPage(request, "Invalid Task!")
    
    if not Task.objects.filter(user = request.user, id = task_id).exists():
        return errorPage(request, "A Corresponding task Doesn't exist!")
    
    if request.method == "POST":
        task = Task.objects.get(user = request.user, id = task_id)
        task.delete()
        messages.success(request, "Task Deleted!")
        
        return redirect("my_tasks")
    
    else:
        return errorPage(request, "This Method is Disallowed")


@authenticated_user
@no_admins
@student_dashboard
def updateProfile(request):
    profile = request.user.profile
    levels = Level.objects.all()
    if request.method == "POST":
        level_id = request.POST.get("level")
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        
        errors = False
        if not (level_id and level_id.isdigit()):
            messages.error(request, "Invalid Level")
            errors = True
        
        if not (email and email.strip()):
            messages.error(request, "Pls, Enter Your Email")
            errors = True
        
        if User.objects.filter(email = email).exclude(id = request.user.id).exists():
            messages.error(request, "Email is Already in use")
            errors = True
            
        if errors:
            return redirect("update_profile")
            
            
        
        level = Level.objects.get(id = level_id )
        
        profile.level = level
        request.user.last_name = last_name
        request.user.first_name = first_name
        request.user.email = email
        profile.is_updated = True
        profile.save()
        request.user.save()
        
        
        messages.success(request, "successfully Updated Profile")
        return redirect("update_profile")
        
    context={
        "levels": levels,
        "page_name":"UPDATE PROFILE",
        "active_name":"update_profile",
        }
    return render(request, "components/update_profile.html", context)


@authenticated_user
@no_admins
@lecturers_only
def updateLecturerProfile(request):
    if request.method == "POST":
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        
        errors = False
        if not (email and email.strip()):
            messages.error(request, "Pls, Enter Your Email")
            errors = True
        
        if User.objects.filter(email = email).exclude(id = request.user.id).exists():
            messages.error(request, "Email is Already in use")
            errors = True
            
        if errors:
            return redirect("update_lecturer_profile")
            
        
        request.user.last_name = last_name
        request.user.first_name = first_name
        request.user.email = email
        
        request.user.profile.is_updated = True
        
        request.user.profile.save()
        request.user.save()
        
        
        messages.success(request, "successfully Updated Profile")
        return redirect("update_lecturer_profile")
        
    context={
        "page_name":"UPDATE PROFILE",
        "active_name":"update_profile",
        }
    return render(request, "components/update_lecturer_profile.html", context)


@authenticated_user
@no_admins
@student_dashboard
def performTask(request, pk):
    if not pk.isdigit():
        return errorPage(request, "Invalid Task!")
    
    if not Task.objects.filter( id = pk).exists():
        return errorPage(request, "A Corresponding task Doesn't exist!")
    
    task = Task.objects.get( id = pk)
    if not task.allow_reply:
        return errorPage(request, "The Task Doesn't Accept Replies")
    
    current_time = datetime.now()
    aware_datetime = timezone.make_aware(current_time)
    
    if aware_datetime > task.due_date:
        task.allow_reply = False
        task.save()
        return errorPage(request, "The Task Has Expired")
    
    if not task.allow_reply:
        return errorPage(request, "The Task Doesn't Allow Replies")
    
    if TaskReply.objects.filter(task = task, student = request.user.profile).exists():
            if not task.allow_edit_response:
                return errorPage(request, "You Have Submitted a Response and Cannot Edit it")
            else:
                response = TaskReply.objects.get(task = task, student = request.user.profile)
                return redirect("edit_response", response.id )
        
    if request.method == "POST":
        response_text = request.POST.get("response-text")
        attachment = request.FILES.get("attach-file")
        
        if not (response_text and response_text.strip() ):
            messages.error(request, "Pls Enter Some Text")        
            return redirect("perform_task", task.id)
        
        if not (task.allow_files and attachment):
            attachmnent = None
            
            
        if not TaskReply.objects.filter(task = task, student = request.user.profile).exists():
            TaskReply.objects.create(
                task = task,
                student = request.user.profile,
                text = response_text,
                attachment = attachment
            )
            messages.success(request, "Response Has Been Sent")
            return redirect("my_responses")
        else:
            if not task.allow_edit_response:
                return errorPage(request, "You Have Submitted a Response and Cannot Edit it")
            else:
                response = TaskReply.objects.get(task = task, student = request.user.profile)
                return redirect("edit_response", response.id )
                
        
    context = {
        "task":task,
        }
    return render(request, "components/perform_task.html", context)


@authenticated_user
@no_admins
@student_dashboard
def studentPastTasks(request):
    student = request.user.profile
    tasks = Task.objects.filter(level = student.level, department = student.department, due_date__lt = datetime.today()).order_by("due_date")
    performed_tasks = []
    student_replies = request.user.profile.taskreply_set.all()
    
    for reply in student_replies:
        performed_tasks.append(reply.task)
    
    context={
        # "active_name":"home",
        "tasks":tasks,
        "performed_tasks":performed_tasks,
        "page_name":"PREVIOUS TASKS",
        "active_name":"previous_tasks",
    }
    return render(request, "components/student_past_tasks.html", context)


@authenticated_user
@no_admins
@student_dashboard
def studentFutureTasks(request):
    student = request.user.profile
    tasks = Task.objects.filter(level = student.level, department = student.department, due_date__gt = datetime.today()).order_by("due_date")
    context={
        "tasks":tasks,
        "page_name":"COMING TASKS",
        "active_name":"coming_tasks",
    }
    return render(request, "components/student_coming_tasks.html", context)




@authenticated_user
@no_admins
@lecturers_only
def lecturerPastTasks(request):
    tasks = Task.objects.filter(user = request.user, due_date__lt = datetime.today()).order_by("due_date")
    context={
        # "active_name":"home",
        "tasks":tasks,
        "page_name":"EXPIRED or PREVIOUS RESPONSES",
        "active_name":"previous_responses",
    }
    return render(request, "components/lecturer_past_tasks.html", context)


@authenticated_user
@no_admins
@lecturers_only
def lecturerFutureTasks(request):
    tasks = Task.objects.filter(user= request.user, due_date__gt = datetime.today()).order_by("due_date")
    context={
        # "active_name":"home",
        "tasks":tasks,
        "page_name":"COMING TASKS",
        "active_name":"coming_tasks",
    }
    return render(request, "components/lecturer_coming_tasks.html", context)


@authenticated_user
@no_admins
@lecturers_only
def viewTaskReplies(request, task_id):
    if not task_id.isdigit():
        return errorPage(request, "Invalid Task!")
    
    if not Task.objects.filter(id = task_id, user = request.user).exists():
        return errorPage(request, "A Corresponding task Doesn't exist!")
    
    task = Task.objects.get( id = task_id)
    
    context = {"task":task}
    return render(request, "components/view_task_replies.html", context)


@authenticated_user
@no_admins
@lecturers_only
def viewResponse(request, response_id):
    if not response_id:
        return errorPage(request, "Invalid Response")
     
    
    if not TaskReply.objects.filter(id = response_id).exists():
        return errorPage(request, "Response not Found")
    
    reply = TaskReply.objects.get(id = response_id)
    
    if reply.task.user != request.user:
        return errorPage(request, "You Cannot View The Reply Because You didn't Create the Task")
        
    
    context = {
        "reply":reply,
        "page_name":"MY RESPONSES",
        "active_name":"my_responses",
        }
    
    return render(request, "components/view_my_response.html", context)
    

@authenticated_user
@no_admins
@student_dashboard
def myResponses(request):
    student = request.user.profile 
    
    replies = TaskReply.objects.filter(student = student)
    
    context = {
        "replies": replies,
        "page_name":"MY RESPONSES",
        "active_name":"my_responses",
        }
    
    return render(request, "components/my_replies.html", context)


@authenticated_user
@no_admins
@student_dashboard
def viewMyResponse(request, response_id):
    if not response_id:
        return errorPage(request, "Invalid Response")
    
    if not TaskReply.objects.filter(id = response_id, student = request.user.profile).exists():
        return errorPage(request, "Response not Found")
    
    reply = TaskReply.objects.get(id = response_id, student = request.user.profile)
    
    context = {
        "reply":reply,
        "page_name":"MY RESPONSES",
        "active_name":"my_responses",
        }
    
    return render(request, "components/view_my_response.html", context)


@authenticated_user
@no_admins
@student_dashboard
def editResponse(request, response_id):
    if not response_id:
        return errorPage(request, "Invalid Response")
    
    if not TaskReply.objects.filter(id = response_id, student = request.user.profile).exists():
        return errorPage(request, "Response not Found")
    
    reply = TaskReply.objects.get(id = response_id, student = request.user.profile)
    
    if not reply.task.allow_edit_response:
        return errorPage(request, "This Task Doesn't Allow Responses to be Edited")
    
    if request.method == "POST":
        response_text = request.POST.get("response-text")
        attachment = request.FILES.get("attach-file")
        
        if not (response_text and response_text.strip() ):
            messages.error(request, "Pls Enter Some Text")        
            return redirect("edit_response", reply.task.id)
        
        if not (reply.task.allow_files and attachment):
            attachmnent = None
            
        if attachment:
            if reply.attachment:
                if hasattr(reply.attachment, "close"):
                    reply.attachment.close()
            reply.attachment.delete()
            
        reply.attachment = attachment
        reply.text = response_text
        reply.save()
        messages.success(request, "Response Updated!")
        return redirect('my_responses')
        
                    
    context = {
        "response":reply,
         "page_name":"MY RESPONSES",
        "active_name":"my_responses",
        }
    
    return render(request, "components/edit_response.html", context)


@authenticated_user
def changePassword(request):
    if request.method == "POST":
        fmrPassword =  request.POST.get("fmr-password")
        newPassword =  request.POST.get("new-password")
        confirmPassword =  request.POST.get("confirm-password")
        
        errors = False
        if not request.user.check_password(fmrPassword):
            messages.error(request, "Incorrect Former Password")
            errors = True

        
        if not newPassword.strip():
            messages.error(request, "Password Cannot be Empty")
            errors = True

        if newPassword != confirmPassword :
            messages.error(request, "The Two new Passwords Don't Match")
            errors = True            
        
        if errors:        
            return redirect("change_password")
        
        request.user.set_password(newPassword)
        request.user.save()
        messages.success(request, "Password Updated!")
        return redirect("change_password")
    
    context = {
        "page_name":"CHANGE PASSWORD",
        "active_name":"change_password",
    }
        
    return render(request, "auth/change_password.html", context)