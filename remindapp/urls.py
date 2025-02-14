from django.urls import path
from remindapp import views

urlpatterns = [
    path("login",views.login, name="login"),
    path("", views.home, name = "dashboard"),
    path("lecturer_dashboard", views.lecturerHome, name = "lecturer_dashboard"),
    path("my_tasks", views.myTasks, name = "my_tasks"),
    path("view_task/<str:pk>", views.viewTasks, name = "view_task"),
    path("add_task", views.addTask, name = "add_task"),
    path("edit_task/<str:pk>", views.editTask, name = "edit_task"),
    path("delete_task/<str:task_id>", views.deleteTask, name = "delete_task"),
    path("perform_task/<str:pk>", views.performTask, name = "perform_task"),
    
    path("update_profile", views.updateProfile, name="update_profile"),
    path("update_lecturer_profile", views.updateLecturerProfile, name="update_lecturer_profile"),
    path("change_password", views.changePassword, name="change_password"),
    
    path("my_responses", views.myResponses, name="my_responses"),
    path("view_my_response/<str:response_id>", views.viewMyResponse, name="view_my_response"),
    path("edit_response/<str:response_id>", views.editResponse, name="edit_response"),
    
    path("student_past_tasks", views.studentPastTasks, name="student_past_tasks"),
    path("student_future_tasks", views.studentFutureTasks, name="student_future_tasks"),
    
    path("lecturer_past_tasks", views.lecturerPastTasks, name="lecturer_past_tasks"),
    path("lecturer_future_tasks", views.lecturerFutureTasks, name="lecturer_future_tasks"),
    
    path("view_task_replies/<str:task_id>", views.viewTaskReplies, name="view_task_replies"),
    path("view_response/<str:response_id>", views.viewResponse, name="view_response"),
    
    path("logout", views.logout, name="logout"),
]
