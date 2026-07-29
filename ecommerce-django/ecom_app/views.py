from http.client import HTTPException

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import forms
from .models import Products, Categories

# Create your views here.
def home(request: HttpRequest):
    products = Products.objects.all()
    categories = Categories.objects.all()
    return render(request, "index.html", {"products": products, "categories": categories})

def about(request: HttpRequest):
    return render(request, "about.html")

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

# Product

def get_product(request: HttpRequest, pk: int):
    product = Products.objects.get(id=pk)
    return render(request, "product.html", {"product": product})

def get_category(request: HttpRequest, cat: str):
    try:
        category = Categories.objects.get(name=cat)
        categories = Categories.objects.all()
        products = Products.objects.filter(category=category)
        return render(request, "category.html", {"products":products, "category":category, "categories": categories})
    except HTTPException as e:
        messages.error(request, "That category doesn't exist")
        return redirect("home")

