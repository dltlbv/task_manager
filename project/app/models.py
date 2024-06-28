from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions_set"
    )
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="projects"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def is_user_part_of_project(self, user):
        return self.owner == user or self.tasks.filter(assigned_to=user).exists()


class Task(models.Model):
    STATUS_CHOICES = [
        ("created", "Создано"),
        ("in_progress", "В процессе"),
        ("done", "Готово"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")

    def __str__(self):
        return self.title

    def is_user_assigned(self, user):
        return self.assigned_to == user
