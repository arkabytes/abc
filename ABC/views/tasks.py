from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ABC.forms import TaskForm, TaskQuickForm
from ABC.models import Task


@login_required
def new_task(request, task_id=None):
    if task_id:
        task = Task.objects.get(pk=task_id)
        form = TaskForm(instance=task)
    else:
        form = TaskForm()

    context = {'form': form, 'task_id': task_id}
    return render(request, 'ABC/new_task.html', context)


@login_required
def tasks(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'ABC/tasks.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new task in quick mode
            form = TaskQuickForm(request.POST, request.FILES)
            if not form.is_valid():
                messages.error(request, 'Some errors has occurred')
                return redirect('tasks')

            form.save()
            messages.success(request, 'Task cread successfully')
            return redirect('tasks')
        else:
            # Add a new task in complete mode (with every field filled)
            form = TaskForm(request.POST, request.FILES)
            if not form.is_valid():
                messages.error(request, 'Some errors has occurred')
                return render(request, 'ABC/new_task.html', {'form': form})

            form.save()
            messages.success(request, 'Task created successfully')
            return redirect('new_task')


@login_required
def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect('tasks')


@login_required
def modify_task(request):
    if request.method == 'POST':
        task_id = request.POST['task_id']
        task = Task.objects.get(pk=task_id)
        # Modify a Task
        form = TaskForm(request.POST, request.FILES, instance=task)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_task.html', {'form': form, 'task_id': task_id})

        form.save()
        return redirect('tasks')