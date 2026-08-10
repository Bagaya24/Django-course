from django.http import HttpRequest

from ecom_app.models import Products, Profile


class Cart:
    def __init__(self, request:HttpRequest):
        self.session = request.session
        # Get request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get("session_key")

        # New user
        if "session_key" not in self.session:
            cart = self.session["session_key"] = {}

        # Make sur the cart works in all pages
        self.cart = cart

    def _save_card_to_db(self):
        if self.request.user.is_authenticated:
            #         get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            cart_transformed = str(self.cart).replace("\'", "\"")

            #         Save the cart transformed to the profile model
            current_user.update(old_cart=cart_transformed)


    def add(self, product, qty:int=1):
        product_id = str(product.id)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = qty
        self.session.modified = True

        #     Deal with log in user
        self._save_card_to_db()


    def add_from_db(self, product, qty:int):
        product_id = str(product)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = qty
        self.session.modified = True
        self._save_card_to_db()

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

        self._save_card_to_db()

    def delete_cart(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        self._save_card_to_db()