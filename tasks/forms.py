from django import forms
from .models import Task, SubTask, Note, Category


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['parent_task', 'title', 'status']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['task', 'content']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']