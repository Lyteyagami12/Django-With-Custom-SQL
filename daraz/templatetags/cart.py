from django import template
from django.shortcuts import render
register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(cart,product):

    # cart = request.session.get('cart')
    keys = cart.keys()
    try:
        for id in keys:
            if int(id) == product.id:
                print(id)
                return True
    except:
        return False
    return False


@register.filter(name='cart_quantity')
def cart_quantity(request,product):
    cart = request.session.get('cart')
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0


@register.filter(name='price_total')
def price_total(request,product):
    cart = request.session.get('cart')
    return product.price * cart_quantity(product, cart)


@register.filter(name='total_cart_price')
def total_cart_price(products , cart):
    sum = 0
    for p in products:
        sum += price_total(p , cart)

    return sum
    