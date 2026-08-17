from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

from cart.cart import Cart
from ecom_app.models import Profile
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem

# Import PayPal stuff
from django.urls import reverse
from django.conf import settings
from uuid import uuid4
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.

def payment_success(request):
    # Delete the cart from the cookie
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]
    return render(request, "payment/payment_success.html")

def payment_failed(request):
    # Delete the cart from the cookie
    # for key in list(request.session.keys()):
    #     if key == "session_key":
    #         del request.session[key]
    return render(request, "payment/payment_failed.html")

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

        # Get host
        host = request.get_host()
        # Create Invoice Number
        my_invoice = str(uuid4())

        # Get shipping info
        my_shipping = request.POST

        request.session["my_shipping"] = my_shipping

        # Gather order info
        full_name = my_shipping.get("shipping_full_name")
        email = my_shipping.get("shipping_email")

        # Create the shipping address from session info
        shipping_address = f"{my_shipping.get('shipping_address1')}\n{my_shipping.get("shipping_address2")}\n{my_shipping.get("shipping_city")}\n{my_shipping.get("shipping_province")}\n{my_shipping.get("shipping_zipcode")}\n{my_shipping.get("shipping_country")}"
        amount_paid = totals

        # Create PayPal from dict
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": totals,
            "item_name": "Computer",
            "no_shipping": "2",
            "invoice": my_invoice,
            "currency_code": "USD",
            "notify_url": f"https://{host}{reverse('paypal-ipn')}",
            "return_url": f"https://{host}{reverse('payment_success')}",
            "cancel_return": f"https://{host}{reverse('payment_failed')}",
        }

        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        # Create a session with shipping info
        my_shipping = request.POST
        request.session["my_shipping"] = my_shipping
        if request.user.is_authenticated:

            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address,
                                 amount_paid=amount_paid, invoice=my_invoice)
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
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user,
                                                      quantity=value, price=price)
                        create_order_item.save()


            # Delete the Cart from the Database
            current_user_profile = Profile.objects.filter(user__id=request.user.id)
            current_user_profile.update(old_cart="")

            return render(request, "payment/billing_info.html",
                          dict(products=products, quantities=quantities, totals=totals, shipping_info=request.POST,
                               billing_form=billing_form, paypal_form=paypal_form))


            # User no logged

        create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address,
                             amount_paid=amount_paid, invoice=my_invoice)
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

        return render(request, "payment/billing_info.html",
                      dict(products=products, quantities=quantities, totals=totals,
                           shipping_info=request.POST, billing_form=billing_form, paypal_form=paypal_form))


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

            # Delete the cart from the cookie
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            # Delete the Cart from the Database
            current_user_profile = Profile.objects.filter(user__id=request.user.id)
            current_user_profile.update(old_cart="")

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

def shipped_dash(request: HttpRequest):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            num = request.POST.get("num")
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
        return render(request, "payment/shipped_dash.html", dict(orders=orders))
    messages.success(request, "Access denied")
    return redirect("home")

def not_shipped_dash(request: HttpRequest):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            num = request.POST.get("num")
            order = Order.objects.filter(id=num)
            order.update(shipped=True)
        return render(request, "payment/not_shipped_dash.html", dict(orders=orders))
    messages.success(request, "Access denied")
    return redirect("home")

def orders(request: HttpRequest, pk: int):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST :
            status = request.POST.get("shipping_status")
            # Get the order
            order = Order.objects.filter(id=pk)
            if status == "true":

                # Update the status
                order.update(shipped=True, date_shipped=datetime.now())
                messages.success(request, "Shipping status Updated")
                return redirect("shipped_dash")
            order.update(shipped=False)
            messages.success(request, "Shipping status Updated")
            return redirect("not_shipped_dash")


        return render(request, "payment/orders.html", dict(order=order, items=items))
    messages.success(request, "Access Denied")
    return redirect("home")
