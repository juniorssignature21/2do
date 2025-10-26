from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Profile, Task
from .forms import TaskForm, RegisterUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.utils import timezone
# Create your views here.

def custom_404(request, exception):
    return render(request, '404.html', status=404)
def home(request):
    tasks = Task.objects.all()
    completed_tasks = Task.objects.filter(completed=True)
    pending_tasks = Task.objects.filter(completed=False)
    current_time = timezone.now()
    
    context = {
        'tasks': tasks,
        'completed_tasks':completed_tasks,
        'pending_tasks':pending_tasks,
        'current_time':current_time,
    }
    return render(request, 'home.html', context)

@login_required(login_url="login")
def add_task(request):
    user = request.user
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            return redirect('home')
        else:
            errors = form.errors
            messages.error(request, "{}".format(errors))
            return redirect('add')
        
    form = TaskForm()
    
    return render(request, 'add_task.html', {
        "form":form,
    })

@login_required(login_url='login')
def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST":
        if form.is_valid():
            completed = request.POST.get('completed')
            if completed:
                task.completed = True
            else:
                task.completed = False
            form.save()
            messages.success(request, "Edited Task!!!")
            return redirect('home')
        else:
            form = TaskForm(instance=task)
            error = form.errors
            messages.success(request, '{}'.format(error))
            return redirect('edit_task', pk=task.id)
    
    return render(request, 'edit_task.html', {
        'task':task,
        'form': form
    })
    
@login_required(login_url='login')
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    messages.success(request, "Deleted Task!!!")
    return redirect('home')
    
    
def signup(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('home')
    
    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(request, email=email, password=password)
            login(request, user)
            messages.success(request, f"Account created for {first_name} {last_name}")
            return redirect('home')
        else:
            errors = form.errors
            messages.error(request, "{}".format(errors))
            return redirect('signup')
    return render(request, 'signup.html', {
        'form':form
    })
    
def login_user(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('home')
    if request.method == "POST":
        get_email = request.POST.get('email')
        get_password = request.POST.get('password')
        myuser = authenticate(email=get_email, password=get_password)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    return render(request, 'login.html')