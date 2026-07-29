from django.http import HttpRequest

from ecom_app.models import Products


class Cart:
    def __init__(self, request:HttpRequest):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get("session_key")

        # New user
        if "session_key" not in self.session:
            cart = self.session['session_key'] = {}

        # Make sur the cart works in all pages
        self.cart = cart

    def add(self, product, qty:int=1):
        product_id = str(product.id)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = qty
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        # Get the ids
        products_ids = self.cart.keys()
        # Use ids to look up the products in the database model
        products = Products.objects.filter(id__in=products_ids)
        return products

    def get_quantities(self):
        return self.cart

    def total_cart(self):
        # get product IDS
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        total = 0
        for key, value in self.cart.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total
    def update_cart(self, product_id, product_quantity: int):
        if product_id in self.cart :
            self.cart[product_id] = product_quantity
        self.session.modified = True

    def delete_cart(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True