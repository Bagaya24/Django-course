from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from ecom_app.models import Products
from .cart import Cart


# Create your views here.
def cart_summary(request:HttpRequest):
    cart = Cart(request)
    products = cart.get_products
    quantities = cart.get_quantities
    return render(request, "cart_summary.html", dict(products=products, quantities=quantities))

def cart_add(request:HttpRequest):
    cart = Cart(request)
    # Test post
    if request.POST.get("action") == "post":
        # Get the stuff
        product_id = int(request.POST.get("product_id"))
        product_qty = request.POST.get("product_qty")
        if product_qty is not None:
            product_qty = int(product_qty)
        # Get the product in the Database
        product = get_object_or_404(Products, id=product_id)
        # Save to the session
        cart.add(product=product, qty=product_qty)

        cart_quantity = cart.__len__()
        return JsonResponse({"quantity": cart_quantity})
    return None

def cart_delete(request:HttpRequest):
    pass

def cart_update(request:HttpRequest):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        # Get the stuff
        product_id = request.POST.get("product_id")
        product_qty = request.POST.get("product_qty")
        if product_qty is not None:
            product_qty = int(product_qty)
        cart.update_cart(product_id=product_id, product_quantity=product_qty)
        return JsonResponse(dict(message="Success"))
    return None