from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, SubTask, Note, Category
from .forms import TaskForm, SubTaskForm, NoteForm, CategoryForm


@login_required
def dashboard(request):
    sort = request.GET.get('sort')

    tasks = Task.objects.all()

    if sort == "date":
        tasks = tasks.order_by('-created_at')
    elif sort == "deadline":
        tasks = tasks.order_by('deadline')
    elif sort == "status":
        tasks = tasks.order_by('status')
    elif sort == "priority":
        tasks = tasks.order_by('priority__name')
    else:
        tasks = tasks.order_by('-created_at')

    tasks = tasks[:5]

    context = {
        'tasks': tasks,
        'total_tasks': Task.objects.count(),
        'pending_tasks': Task.objects.filter(status="Pending").count(),
        'in_progress_tasks': Task.objects.filter(status="In Progress").count(),
        'completed_tasks': Task.objects.filter(status="Completed").count(),
    }

    return render(request, 'tasks/dashboard.html', context)


@login_required
def task_list(request):
    sort = request.GET.get('sort')

    tasks = Task.objects.all()

    if sort == "date":
        tasks = tasks.order_by('-created_at')
    elif sort == "priority":
        tasks = tasks.order_by('priority__name')
    elif sort == "status":
        tasks = tasks.order_by('status')
    elif sort == "title":
        tasks = tasks.order_by('title')
    elif sort == "high":
        tasks = tasks.filter(priority__name="High")
    elif sort == "medium":
        tasks = tasks.filter(priority__name="Medium")
    elif sort == "low":
        tasks = tasks.filter(priority__name="Low")
    elif sort == "critical":
        tasks = tasks.filter(priority__name="Critical")
    elif sort == "optional":
        tasks = tasks.filter(priority__name="Optional")

    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    subtasks = SubTask.objects.filter(parent_task=task)
    notes = Note.objects.filter(task=task)

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'subtasks': subtasks,
        'notes': notes,
    })


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('task_list')

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Add Task'
    })


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        return redirect('task_detail', pk=task.pk)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Edit Task'
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {
        'task': task
    })


@login_required
def mark_task_completed(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = "Completed"
    task.save()
    return redirect('task_list')


@login_required
def subtask_list(request):
    search = request.GET.get('search')
    status = request.GET.get('status')
    sort = request.GET.get('sort')

    subtasks = SubTask.objects.all()

    if search:
        subtasks = subtasks.filter(title__icontains=search)

    if status:
        subtasks = subtasks.filter(status=status)

    if sort == "title":
        subtasks = subtasks.order_by('title')
    elif sort == "status":
        subtasks = subtasks.order_by('status')
    elif sort == "date":
        subtasks = subtasks.order_by('-created_at')
    else:
        subtasks = subtasks.order_by('-created_at')

    return render(request, "tasks/subtask_list.html", {
        "subtasks": subtasks
    })


@login_required
def subtask_create(request):
    form = SubTaskForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('subtask_list')

    return render(request, 'tasks/subtask_form.html', {
        'form': form,
        'title': 'Add SubTask'
    })


@login_required
def subtask_update(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    form = SubTaskForm(request.POST or None, instance=subtask)

    if form.is_valid():
        form.save()
        return redirect('subtask_list')

    return render(request, 'tasks/subtask_form.html', {
        'form': form,
        'title': 'Edit SubTask'
    })


@login_required
def subtask_delete(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)

    if request.method == 'POST':
        subtask.delete()
        return redirect('subtask_list')

    return render(request, 'tasks/subtask_confirm_delete.html', {
        'subtask': subtask
    })


@login_required
def note_list(request):
    search = request.GET.get('search')
    created_at = request.GET.get('created_at')
    sort = request.GET.get('sort')

    notes = Note.objects.all()

    if search:
        notes = notes.filter(content__icontains=search)

    if created_at:
        notes = notes.filter(created_at__date=created_at)

    if sort == "date":
        notes = notes.order_by('-created_at')
    elif sort == "task":
        notes = notes.order_by('task__title')
    else:
        notes = notes.order_by('-created_at')

    return render(request, "tasks/note_list.html", {
        "notes": notes
    })


@login_required
def note_create(request):
    form = NoteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('note_list')

    return render(request, 'tasks/note_form.html', {
        'form': form,
        'title': 'Add Note'
    })


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = NoteForm(request.POST or None, instance=note)

    if form.is_valid():
        form.save()
        return redirect('note_list')

    return render(request, 'tasks/note_form.html', {
        'form': form,
        'title': 'Edit Note'
    })


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        note.delete()
        return redirect('note_list')

    return render(request, 'tasks/note_confirm_delete.html', {
        'note': note
    })


@login_required
def category_list(request):
    search = request.GET.get('search')
    sort = request.GET.get('sort')

    categories = Category.objects.all()

    if search:
        categories = categories.filter(name__icontains=search)

    if sort == "name_desc":
        categories = categories.order_by('-name')
    else:
        categories = categories.order_by('name')

    return render(request, "tasks/category_list.html", {
        "categories": categories
    })


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'tasks/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'tasks/category_form.html', {
        'form': form,
        'title': 'Edit Category'
    })


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('category_list')

    return render(request, 'tasks/category_confirm_delete.html', {
        'category': category
    })