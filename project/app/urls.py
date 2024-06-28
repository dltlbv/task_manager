from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home,
    register,
    profile,
    projects_list,
    project_detail,
    project_create,
    project_edit,
    project_delete,
    task_edit,
    task_create,
    task_delete,
)

urlpatterns = [
    path("", home, name="home"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="app/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="app/logout.html"),
        name="logout",
    ),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("projects/", projects_list, name="projects_list"),
    path("projects/<int:pk>/", project_detail, name="project_detail"),
    path("project_create/", project_create, name="project_create"),
    path("project_edit/<int:pk>/", project_edit, name="project_edit"),
    path("project_delete/<int:pk>/", project_delete, name="project_delete"),
    path("tasks/<int:pk>/edit/", task_edit, name="task_edit"),
    path("tasks/<int:pk>/delete/", task_delete, name="task_delete"),
    path("projects/<int:project_pk>/tasks/create/", task_create, name="task_create"),
]
