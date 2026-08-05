from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages

from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress


# Create your views here.

def payment_success(request:HttpRequest):
    return render(request, "payment/payment_success.html")

def checkout(request:HttpRequest):
    cart = Cart(request)
    products = cart.get_products
    quantities = cart.get_quantities
    totals = cart.total_cart()

    if request.user.is_authenticated:
    #     checkout as logged user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html",
                      dict(products=products, quantities=quantities, totals=totals, shipping_form=shipping_form))

    shipping_form = ShippingForm(request.POST or None)
    return render(request, "payment/checkout.html",
                  dict(products=products, quantities=quantities, totals=totals, shipping_form=shipping_form))

def billing_info(request:HttpRequest):
    if request.method == "POST":
        cart = Cart(request)
        products = cart.get_products
        quantities = cart.get_quantities
        totals = cart.total_cart()
        billing_form = PaymentForm()
        if request.user.is_authenticated:

            return render(request, "payment/billing_info.html",
                          dict(products=products, quantities=quantities, totals=totals, shipping_info=request.POST,
                               billing_form=billing_form))

        return render(request, "payment/billing_info.html",
                      dict(products=products, quantities=quantities, totals=totals, shipping_info=request.POST ,billing_form=billing_form))
    messages.success(request, "Access Denied")
    return redirect("home")

