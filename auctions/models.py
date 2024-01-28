from types import MappingProxyType
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ManyToManyField


class User(AbstractUser):
    pass

class listing(models.Model):
    listingid = models.AutoField(auto_created=True,primary_key=True)
    title = models.CharField(max_length=200)
    starting_amount = models.PositiveBigIntegerField(default=0)
    description = models.CharField(max_length=1000)
    #category = models.ManyToManyField("category", verbose_name=("category"))
    category = models.ForeignKey("category", on_delete=models.CASCADE, default=1)
    userid = models.ForeignKey("User", verbose_name=("userid"), on_delete=models.CASCADE,related_name = "created_user")
    img_url = models.CharField(max_length=1000, default=None, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    #winner = models.ForeignKey("User", verbose_name=("winner"), on_delete=models.CASCADE, default = 'NULL',null=True, related_name = "winner")
    #winner = ManyToManyField(User,null=True)
    def __srt__(self):
        return self.listingid,self.title
    
class category(models.Model):
    category_id = models.AutoField(auto_created=True,primary_key=True)
    category_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.category_name
    
class bids(models.Model):
    bid_id = models.AutoField(auto_created=True,primary_key=True)
    bid_amount = models.PositiveBigIntegerField(default=0)
    listing= models.ForeignKey("listing", verbose_name=("listingid"), on_delete=models.CASCADE, default=0)
    user = models.ForeignKey("User", verbose_name=("userid"), on_delete=models.CASCADE)
    
    
class winner(models.Model):
    winner_id = models.AutoField(auto_created=True,primary_key=True)
    user = models.ForeignKey("User", verbose_name=("winner_user"), on_delete=models.CASCADE)
    listing = models.ForeignKey("listing", verbose_name=("listing"), on_delete=models.CASCADE,default=0)
    
    
class comments(models.Model):
    comment = models.CharField(max_length=1000)
    product = models.ForeignKey("listing", verbose_name=("product"), on_delete=models.CASCADE)
    user = models.ForeignKey("User", verbose_name=("winner_user"), on_delete=models.CASCADE)
    
class watchlist(models.Model):
    product = models.ForeignKey("listing", verbose_name=("product"), on_delete=models.CASCADE)
    user = models.ForeignKey("User", verbose_name=("winner_user"), on_delete=models.CASCADE)