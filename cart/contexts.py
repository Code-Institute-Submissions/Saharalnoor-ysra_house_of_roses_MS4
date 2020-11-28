from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """ Makes the cart content available across the whole website """

    cart_items = []
    total = 0
    items_count = 0
    cart = request.session.get('cart', {})
    print(cart)

    for item_id, item_data in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += item_data * product.price
        items_count += item_data
        cart_items.append({
            'product': product,
            'item_id': item_id,
            'quantity': item_data
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'grand_total': grand_total,
        'items_count': items_count,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'delivery': delivery,
    }

    print(context)
    print(cart_items)

    return context