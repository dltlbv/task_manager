from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Project, Task
from django.utils import timezone


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован")
        return email


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description"]
        labels = {
            "title": "Название",
            "description": "Описание",
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "due_date", "status"]
        labels = {
            "title": "Название",
            "description": "Описание",
            "assigned_to": "Назначено пользователю",
            "due_date": "Срок выполнения",
            "status": "Статус",
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date <= timezone.now():
            raise ValidationError("Срок выполнения должен быть в будущем")
        return due_date


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["status"]
        labels = {
            "status": "Статус",
        }
