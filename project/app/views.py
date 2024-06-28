from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, ProjectForm, TaskForm, TaskStatusForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Project, Task
from django.http import HttpResponseForbidden


def home(request):
    return render(request, "app/index.html")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserRegistrationForm()

    return render(request, "app/register.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    projects = Project.objects.filter(owner=user)
    return render(request, "app/profile.html", {"user": user, "projects": projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    is_owner = request.user == project.owner
    is_assigned = tasks.filter(assigned_to=request.user).exists()
    if not is_owner and not is_assigned:
        return HttpResponseForbidden("Доступ запрещен")
    return render(
        request,
        "app/project_detail.html",
        {
            "project": project,
            "tasks": tasks,
            "is_owner": is_owner,
        },
    )


@login_required
def projects_list(request):
    user_tasks = Task.objects.filter(assigned_to=request.user)
    user_projects = Project.objects.filter(tasks__in=user_tasks).distinct()
    return render(
        request,
        "app/projects_list.html",
        {
            "projects": user_projects,
            "user_tasks": user_tasks,
            "current_user": request.user,
        },
    )


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect("project_detail", pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, "app/project_create.html", {"form": form})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects_list")
    else:
        form = ProjectForm(instance=project)
    return render(request, "app/project_edit.html", {"form": form, "project": project})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects_list")
    return render(request, "app/project_delete.html", {"project": project})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    is_owner = request.user == task.project.owner
    is_assigned = request.user == task.assigned_to
    if not is_owner and not is_assigned:
        return HttpResponseForbidden("Доступ запрещен")
    if request.method == "POST":
        if is_owner:
            form = TaskForm(request.POST, instance=task)
        else:
            form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("project_detail", pk=task.project.pk)
    else:
        if is_owner:
            form = TaskForm(instance=task)
        else:
            form = TaskStatusForm(instance=task)
    return render(
        request,
        "app/task_edit.html",
        {"form": form, "task": task, "is_owner": is_owner},
    )


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk
    if request.method == "POST":
        task.delete()
        return redirect("project_detail", pk=project_pk)
    return render(request, "app/task_delete.html", {"task": task})


@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("project_detail", pk=project.pk)
    else:
        form = TaskForm()
    return render(request, "app/task_create.html", {"form": form})
