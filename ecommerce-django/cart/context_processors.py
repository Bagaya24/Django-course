from django.http import HttpRequest

from .cart import Cart

# Write the context processor so that the cart session can work in all pages
def cart(request:HttpRequest):
    return {"cart": Cart(request)}