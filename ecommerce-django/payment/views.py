from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem


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

        # Create a session with shipping info
        my_shipping = request.POST
        request.session["my_shipping"] = my_shipping
        if request.user.is_authenticated:

            return render(request, "payment/billing_info.html",
                          dict(products=products, quantities=quantities, totals=totals, shipping_info=request.POST,
                               billing_form=billing_form))

        return render(request, "payment/billing_info.html",
                      dict(products=products, quantities=quantities, totals=totals, shipping_info=request.POST ,billing_form=billing_form))
    messages.success(request, "Access Denied")
    return redirect("home")

def process_order(request:HttpRequest):
    if request.POST:
        cart = Cart(request)
        products = cart.get_products
        quantities = cart.get_quantities
        totals = cart.total_cart()
        # Get Billing info for last page
        payment_form = PaymentForm(request.POST or None)

        # Get shipping  session date
        my_shipping = request.session.get("my_shipping")

        # Gather order info
        full_name = my_shipping.get("shipping_full_name")
        email = my_shipping.get("shipping_email")

        # Create the shipping address from session info
        shipping_address = f"{my_shipping.get('shipping_address1')}\n{my_shipping.get("shipping_address2")}\n{my_shipping.get("shipping_city")}\n{my_shipping.get("shipping_province")}\n{my_shipping.get("shipping_zipcode")}\n{my_shipping.get("shipping_country")}"
        amount_paid = totals

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
            order_id = create_order.pk
            # Get products info
            for product in products():
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price

                for key, value in quantities().items():
                    if int(key) == product_id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
                        # cart.delete_cart(product_id=product_id)

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "order placed!")
            return render(request, "payment/process_order.html")

        # User no logged
        create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address,
                                 amount_paid=amount_paid)
        create_order.save()
        order_id = create_order.pk
        for product in products():
            product_id = product.id
            price = product.sale_price if product.is_sale else product.price

            for key, value in quantities().items():
                if int(key) == product_id:
                    # Create order item
                    create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                    create_order_item.save()
                    # cart.delete_cart(product_id=product_id)

        for key in list(request.session.keys()):
            if key == "session_key":
                del request.session[key]
        messages.success(request, "order placed!")
        return render(request, "payment/process_order.html")

    messages.error(request, "Access Denied")
    return redirect("home")
