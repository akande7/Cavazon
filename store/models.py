from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

#creating the Customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

#creating the Product model
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price=models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url= ''
        return url            

#creating the Order model
class Order(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete =  models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200, null=True) 

    def __str__(self):
        return str(self.transaction_id)     

    @property
    # A function to get the total price for all items in the cart
    def get_cart_total(self):
        orderitems =self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    # A function to get the total amount of items in the cart
    def get_cart_items(self):
        orderitems =self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total    

#creating the OrderItem model
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

# A function to get the total numbers of items ordered
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

#creating the shipping address model      
class ShippingAddress(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address