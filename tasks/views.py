from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # print(request.POST)
            try:
                # register user...
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                # Creamos el cooking...
                login(request, user)
                return redirect("task")
                # return HttpResponse("User created sussefully")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Usename already exists"},
                )

        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Password do not macth"},
        )


@login_required
def task2(request):
    tareas = task.objects.filter(user=request.user, datecomplete__isnull=True)
    return render(request, "task.html", {"tareas": tareas})


@login_required
def task_completed(request):
    tareas = task.objects.filter(
        user=request.user, datecomplete__isnull=False
    ).order_by("-datecomplete")
    return render(request, "task.html", {"tareas": tareas})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("task")
        except:
            return render(
                request,
                "create_task.html",
                {"form": TaskForm, "error": "Please provide valid data"},
            )


@login_required
def task_detail(request, task_id):
    tareas = get_object_or_404(task, pk=task_id, user=request.user)
    form = TaskForm(instance=tareas)
    if request.method == "GET":
        return render(request, "task_detail.html", {"tareas": tareas, "form": form})
    else:
        try:
            tareas = get_object_or_404(task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=tareas)
            form.save()
            return redirect("task")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {"tareas": tareas, "form": form, "error": ValueError},
            )


@login_required
def complete_task(request, task_id):
    tareas = get_object_or_404(task, pk=task_id, user=request.user)
    if request.method == "GET":
        return redirect("task")
    else:
        tareas.datecomplete = timezone.now()
        tareas.save()
        return redirect("task")


@login_required
def delete_task(request, task_id):
    tareas = get_object_or_404(task, pk=task_id, user=request.user)
    if request.method == "GET":
        return redirect("task")
    else:
        tareas.delete()
        return redirect("task")


@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        # valida que exista el usuario en la tabla...
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        # si el username o password es incorrecto...
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Alert: Username or password is incorrect...",
                },
            )
        else:
            login(request, user)
            return redirect("task")
