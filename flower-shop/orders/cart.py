# orders/cart.py
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, bouquet_id, quantity=1, override_quantity=False):
        bouquet_id = str(bouquet_id)
        if bouquet_id not in self.cart:
            self.cart[bouquet_id] = {'quantity': 0}
        if override_quantity:
            self.cart[bouquet_id]['quantity'] = quantity
        else:
            self.cart[bouquet_id]['quantity'] += quantity
        self.save()

    def remove(self, bouquet_id):
        bouquet_id = str(bouquet_id)
        if bouquet_id in self.cart:
            del self.cart[bouquet_id]
            self.save()

    def __iter__(self):
        from catalog.models import Bouquet
        bouquet_ids = self.cart.keys()
        bouquets = Bouquet.objects.filter(id__in=bouquet_ids)
        cart = self.cart.copy()
        for bouquet in bouquets:
            cart[str(bouquet.id)]['bouquet'] = bouquet
            cart[str(bouquet.id)]['total_price'] = bouquet.price * cart[str(bouquet.id)]['quantity']
        for item in cart.values():
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        from catalog.models import Bouquet
        return sum(
            Bouquet.objects.get(id=item_id).price * item['quantity']
            for item_id, item in self.cart.items()
        )

    def clear(self):
        del self.session['cart']
        self.save()

    def save(self):
        self.session.modified = True