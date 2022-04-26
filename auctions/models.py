from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


"""
Models: Your application should have at least three models in addition to the User model:
one for auction listings, one for bids, and one for comments made on auction listings.
It’s up to you to decide what fields each model should have, and what the types of those fields should be.
You may have additional models if you would like.
"""

# CATEGORIES: id | category
class Category(models.Model):
    category = models.CharField(max_length=64)
    
    def __str__(self):
        return f"Category: {self.category}"


# PRODUCTS: id | user_id | title | image | description | price | current_bid | status | category
class Product(models.Model):
    title = models.CharField(max_length=64)
    image = models.TextField(max_length=300)
    description = models.TextField(max_length=300)
    price = models.IntegerField()
    current_bid = models.IntegerField(blank=True, default="0")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id_prods")
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_name", blank=True, default="1")
    watchedby = models.ManyToManyField(User, blank=True, related_name="watchedby")

    def __str__(self):
        return f"{self.title} (init. price {self.price} - current bid {self.current_bid}), posted by {self.user_id} (active?: {self.status}). Category: {self.category}"


# BIDS: user_id | product_id | amount
class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id_bids")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_id_bids")
    bid = models.IntegerField()

    def __str__(self):
        return f"User {self.user_id} bid {self.bid} on product {self.product_id}"


# COMMENTS: user_id | product_id | comment
class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id_comments")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_id_comments")
    comment = models.TextField(max_length=300)

    def __str__(self):
        return f"User {self.user_id} commented on product {self.product_id}: '{self.comment}'"
