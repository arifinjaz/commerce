from itertools import product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import urllib
from PIL import Image
import requests
from io import BytesIO
from django.contrib.auth.decorators import login_required
from .models import User, listing, category,bids, winner, comments,watchlist
#from .forms import comment_form as f
from django import forms

class comment_form(forms.Form):
    #comment = forms.CharField(widget=forms.Textarea)
    your_name = forms.CharField(label='Your name', max_length=100)


#@login_required
def active_listing (request):
    if request.method == "POST":
        item = request.POST["category"]
        print(f'item is {item}')
        cateid = category.objects.values_list('category_id').filter(category_name = item)
        cateid = [item for t in cateid for item in t][0]
        print(cateid)
        data = listing.objects.all().filter(category = cateid,is_active = True)
        print(data)
        return render(request, "auctions/active_listing.html",{
        "data" : data
        }
        )
    data = listing.objects.all()#.filter(is_active = True)
    
    amount = bids.objects.order_by('listing', 'bid_amount' )
    #print(amount)
    
    amt = {}
    for a in amount:
        amt.update({a.listing: a.bid_amount})
        #print(amt)
    print(amt)
    
    
    for d in data:
        if amt.get(d):
            d.starting_amount = amt.get(d)
       
    
    # for a in amount:
    #     print(a)
    # for i in range(len(data)):
    #     d= data[i]
    #     if amount[i].listing in
    #         print(d.starting_amount)
    
    #FruitBasket.objects.order_by('fruit', '-count').distinct('fruit')
    print(f'amount{amount[0].listing}')
    return render(request, "auctions/active_listing.html",{
        "data" : data
        #"amount":amount
    }
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("active_listing"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("active_listing"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("active_listing"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    print(request.user.id)
    categ = category.objects.filter()
    i=[]
    for item in category.objects.filter():
        print(item)
        i.append(item)
        print(i)
    #print(categ)
    if request.method == "POST":
        r = request.POST
        listing_name = r["product"]
        amount = r["starting"]
        c = r["category"]
        print(c)
        cate = category.objects.get(category_name = c)
        print(cate.category_id)
        url = r["img"]
        description = r["description"]
        
        new = listing.objects.create(title=listing_name, starting_amount = amount, description = description, category = cate, userid_id =request.user.id,
                                     img_url = url )
        
        #new = listing.objects.create(listing_name, amount, description, cate)
        new.save()

    return render (request, "auctions/listing.html",{
        "category":categ
    })



def selected_listing (request):
    if request.method == "POST":
        print(request.POST["user"])
        data = listing.objects.get(listingid = request.POST["listingid"])
        new_bid = request.POST["bid_amount"]
        #l = listing.objects.get(listingid = request.POST["listingid"])
        bids_data = bids.objects.filter(listing = listing.objects.get(listingid = request.POST["listingid"])
                                        ).order_by("-bid_amount")[:1]
        print(data.starting_amount)
        #for bid in bids_data:
         #   print(bid.bid_amount)
        #print(bids_data[0])
        
        
        if bids_data:
            if int(new_bid) < int(bids_data[0].bid_amount):
                messages.warning(request,f"amount lesser than the highest bid, please enter a higher than ${bids_data[0].bid_amount}!!")
                return render (request, "auctions/selected_listing.html",{
                "data":data,
                "highest_bid":bids_data[0].bid_amount
                })
                
        elif int(new_bid) < data.starting_amount:
            messages.warning(request,f"amount lesser than the Staring / Base Amount, please enter a value higher than ${data.starting_amount}!!")
            return render (request, "auctions/selected_listing.html",{
            "data":data}) 
        #save bid
        
        bid_amount = bids.objects.create(
            bid_amount = request.POST["bid_amount"],
            listing = listing.objects.get(listingid = request.POST["listingid"]),
            user = request.user
            )
        bid_amount.save()  
       
        return render (request, "auctions/selected_listing.html",{
        "data":data,
        "highest_bid":request.POST["bid_amount"]
    })
    else:
        come = request.GET.getlist('comment',default=None)
        item = request.GET['selected']
        user = request.user
        exists = None
        if not user.id == None:
            watch = watchlist.objects.all().filter(product = item).filter(user = request.user).distinct()
            if watch:
                exists = "yes"
            else:
                exists = "no"
                
        if come:
            com = comments.objects.create(comment = request.GET['comment'],
                product = listing.objects.get(listingid=item),
                user = request.user
                )
            com.save()
        #comment = comments.objects.values_list('comment','user')
        comment = comments.objects.filter(product = item).order_by('-id')
        
        #print(comment)
        
        data = listing.objects.get(listingid=item)
        bids_data = bids.objects.filter(listing = data).order_by("-bid_amount")[:1]
        #print(bids_data[0].bid_amount)
        
        
        #To handle Bid values
        if bids_data:
            return render (request, "auctions/selected_listing.html",{
                "data":data,
                "highest_bid": bids_data[0].bid_amount,
                "comment":comment,
                "watch":exists
            })
        else:
            return render (request, "auctions/selected_listing.html",{
                "data":data,
                "comment":comment,
                "watch":exists
            })
            
            
            
            
def end_listing(request):
    if request.method == "POST":
        h_bid = bids.objects.filter(listing = listing.objects.get(listingid = request.POST["listingid"])).order_by("-bid_amount")[:1]
        if h_bid:
            #1) declare a winner
            win = winner.objects.create(user = h_bid[0].user, listing = h_bid[0].listing)
            win.save()
        #2) Deactivate the listing
        active = listing.objects.get(listingid = request.POST["listingid"])
        print('yes this is post end_listing')
        print(active.is_active)
        active.is_active = False
        active.save(update_fields=['is_active'])
    return HttpResponseRedirect(reverse("active_listing"))
    

def watch(request):
    if request.method == "POST":
        item = request.POST["watch"]
        watchlist.objects.all().filter(product = item).filter(user = request.user).delete()
    
    item = request.GET.getlist('watch',default=None)
    if item == []:
        print ("empty")
    else:
        watch = watchlist.objects.create(product = listing.objects.get(listingid=item[0]),
            user = request.user
            )
        watch.save()
    li = watchlist.objects.values_list('product').filter(user = request.user).distinct()
    li = [item for t in li for item in t]
    print(li)
    data = listing.objects.all().filter(listingid__in=(li))
    #data = watchlist.objects.all().filter(user = request.user).distinct()

    # print(data)
    # for d in data:
    #     print(d.product.title)
        
    return render(request, "auctions/watchlist.html",{
        "data" : data
    }
    )
    
def categories(request):
    all = category.objects.all()
    
    return render(request, "auctions/categories.html",{
        "categories":all
    })