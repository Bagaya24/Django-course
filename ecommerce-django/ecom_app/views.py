from http.client import HTTPException
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
import json

from cart.cart import Cart

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from . import forms
from .models import Products, Categories, Profile


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
            # Cart stuff
            current_user_profile = Profile.objects.get(user__id=request.user.id)
            # Get their saved card from database
            saved_cart = current_user_profile.old_cart
            # convert database string to python dict
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                #     Add the loaded cart dictionary to our section
                cart = Cart(request)
                 # Loop throw the cart and add the items from the database
                for key, value in converted_cart.items():
                    cart.add_from_db(product=key, qty=value)

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
            messages.success(request, "You account has created, please ... !")
            return redirect("user_info")
        messages.error(request, "Some things whet wrong, please make sure all the fields are ...")
    return render(request, "register.html", {"form":form})

def update_user(request):
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

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == "POST":
            form = forms.UpdatePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been update")
                login(request, current_user)
                return redirect("update_user")
            for error in list(form.errors.values()):
                messages.error(request, error)


        form = forms.UpdatePasswordForm(current_user)
        return render(request, "update_password.html", {"form": form})

    messages.success(request, "You must be logged in to access that page")
    return redirect("home")

def update_info(request):
    if request.user.is_authenticated:
        # Get current user
        current_user = forms.Profile.objects.get(user__id=request.user.id)
        # Get current user's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get user's shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        form = forms.UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your info has been updated!")
            return redirect("home")
        return render(request, "update_user_info.html",
                      {"form": form, "shipping_form": shipping_form})
    messages.success(request, "You must be logged in to access that page!")
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

def search(request:HttpRequest):
    # Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST.get("search")
        # Query the products BD model

        searched = Products.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.error(request, "Sorry, we don't have this product")
        return render(request, "search.html", {"searched":searched})
    return render(request, "search.html")