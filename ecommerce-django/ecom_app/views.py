from http.client import HTTPException
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from . import forms
from .models import Products, Categories

# Create your views here.
def home(request: HttpRequest):
    products = Products.objects.all()
    categories = Categories.objects.all()
    menu_categories = Categories.objects.all()[0:2]
    return render(request, "index.html",
                  {"products": products, "categories": categories, "menu_categories":menu_categories})

def about(request: HttpRequest):
    menu_categories = Categories.objects.all()[0:2]
    return render(request, "about.html", {"menu_categories":menu_categories})

# User
def login_user(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You logged in")
            return redirect("home")
        messages.error(request, "Your password or your Email are incorrect")
    return render(request, "login.html")

def logout_user(request: HttpRequest):
    logout(request)
    messages.success(request, "You have been logout")
    return redirect("home")

def register_user(request: HttpRequest):
    form = forms.SignUpForm()
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered successfully !")
            return redirect("home")
        messages.error(request, "Some things whet wrong, please make sure all the fields are ...")
    return render(request, "register.html", {"form":form})

def update_user(request: HttpRequest):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = forms.UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User has been Update!")
            return  redirect('home')
        return render(request, "update_user.html", {"form":user_form})

    messages.success(request, "You must be logged in to access that page")
    return redirect("home")

# Product

def get_product(request: HttpRequest, pk: int):
    product = Products.objects.get(id=pk)
    menu_categories = Categories.objects.all()[0:2]
    return render(request, "product.html", {"product": product, "menu_categories":menu_categories})

# Category
def get_category(request: HttpRequest, cat: str):
    try:
        category = Categories.objects.get(name=cat)
        categories = Categories.objects.all()
        menu_categories = Categories.objects.all()[0:2]
        products = Products.objects.filter(category=category)
        return render(request, "category.html",
                      {"products":products, "category":category, "categories": categories, "menu_categories":menu_categories})
    except HTTPException as e:
        messages.error(request, "That category doesn't exist")
        return redirect("home")

def get_category_summary(request:HttpRequest):
    try:
        categories = Categories.objects.all()
        menu_categories = Categories.objects.all()[0:2]
        return render(request, "category_summary.html", {"categories": categories, "menu_categories":menu_categories})
    except HTTPException as e:
        pass
