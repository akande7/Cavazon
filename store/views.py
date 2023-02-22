from urllib import request
from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import *

#created view for store
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

#created view for cart
def cart(request):
    # checking if user is authenticated 
    if request.user.is_authenticated: 
        Customer = request.user.customer
        # creating an order or getting exsiting order for a customer
        order, created =  Order.objects.get_or_create(Customer=Customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_item':0 }

    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)

#created view for checkout
def checkout(request):
    # checking if user is authenticated 
    if request.user.is_authenticated: 
        Customer = request.user.customer
        # creating an order or getting exsiting order for a customer
        order, created =  Order.objects.get_or_create(Customer=Customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_item':0 }

    context = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', context)



#created view for product
def product(request):

    context = {}
    return render(request, 'store/product.html', context )  

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)