from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class User(AbstractUser):
    pass

#1. LISTING
# Title of item
#Description
#Starting price
#Current price
#Image URL (optional)
#Category
#Is it active or closed?
#Owner (who created it) 

class Listing(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits = 10,decimal_places = 2)
    current_price = models.DecimalField(max_digits = 10,decimal_places = 2)
    image_URL = models.URLField()
    category = models.CharField()
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
              return self.title
    #2. settings.AUTH_USER_MODEL
    #Refers to the User model used in project
     #Default → auth.User
     ##Custom → auctions.User

     #2. BIDS
     
class Bids(models.Model):
      listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="bids")
      user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      timestamp = models.DateTimeField(auto_now_add=True)
      def __str__(self):
         return f"{self.user} bid ₹{self.amount} on {self.listings}"
#2.Comments
class Comment(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
              return self.amount

class WatchList(models.Model):
                        # WHO is watching?
                        owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
                        
                        # WHAT are they watching?
                        listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)

       

