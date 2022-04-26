from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect # redirect added by me
from django.urls import reverse
from django.contrib.auth.decorators import login_required # added by me
from django import forms # added by me

from .models import User, Category, Product, Bid, Comment


""" Create a class for the form to create a listing """
class CreateForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title of the item', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write a description of the item', 'class': 'form-control'}))
    image = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Provide a link for the image', 'class': 'form-control'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control width20'}))



def index(request):
    
    # get the details from the ACTIVE listings to pass to the template:
    # title, image, description, user that posted it, price and bid
    products = Product.objects.filter(status=True)

    return render(request, "auctions/index.html", {
        "products": products
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# to generate the page of a listing
def productpage(request, product_title, message=""):
    
    # if redirected here bc the bid was not accepted:
    error = False
    if message:
        error = "Bid amount is insufficient."

    # get the info of the product:
    product = Product.objects.get(title=product_title)

    # if the user tries to reach a product that doesn't exist
    if not product:
        return HttpResponseRedirect(reverse("index"))


    # REGARDLESS OF WHETHER OR NOT THE USER iS LOGGED IN:

    # get the comments of the product
    comments = Comment.objects.filter(product_id=product.id)

    # declare the vars to be populated/updated depending on the following ifs/elses
    active = "a"
    author = False
    watchlist = "b"
    winner = "c"
    winnerforauthor = False
    winnerlogged = False

    # distinguish if the listing is active or not:
    if product.status == True:
        active = True

        # if the user is logged in...
        if request.user.is_authenticated:

            userinfo = User.objects.get(username=request.user)

            # find out if they're the author of the post
            if userinfo == product.user_id:
                author = True

            # find out if they have this product on their watchlist or not
            if Product.objects.filter(title=product_title, watchedby=userinfo):
                watchlist = True
            else:
                watchlist = False

    # else: if the listing is NOT active  
    else:
        active = False

        # if the user is logged in, see if they're the winner to display it on the template
        if request.user.is_authenticated:

            userinfo = User.objects.get(username=request.user)

            # find out if they person seeing the closed listing is the author
            if userinfo == product.user_id:
                author = True

            winningbid = Bid.objects.get(bid=product.current_bid, product_id=product.id)

            # save who the winner is so it can show when the author closes a listing
            winnerforauthor = winningbid.user_id

            if winningbid.user_id == userinfo:
                winnerlogged = True
            else:
                winnerlogged = False

    return render(request, "auctions/productpage.html", {
        "product": product,
        "comments": comments,
        "active": active,
        "author": author,
        "watchlist": watchlist,
        "winner": winner,
        "winnerforauthor": winnerforauthor,
        "winnerlogged": winnerlogged,
        "error": error
    })


# Add or Remove to/from the Watchlist
@login_required
def watchlistaddremove(request, product_title):

    # get the info of the product:
    product = Product.objects.get(title=product_title)

    # get the info of the user:
    userinfo = User.objects.get(username=request.user)

    # find out if they have this product on their watchlist or not:
    # if they do, remove it
    if Product.objects.filter(title=product_title, watchedby=userinfo):

        product.watchedby.remove(userinfo)

    # if they don't, add it
    else:

        product.watchedby.add(userinfo)

    # return the user to the page of the product
    return redirect(productpage, product_title=product.title)


# to close a listing (only possible by its author)
@login_required
def closelisting(request, product_title):

    # get the info of the product:
    product = Product.objects.get(title=product_title)

    # change the status of the product
    product.status = False

    # save the changes
    product.save()

    # return the user to the page of the product
    return redirect(productpage, product_title=product.title)


# to handle the bids
@login_required
def bidding(request, product_title):

    # get the info from the form (that is, the bid amount)
    bid = int(request.GET["bid"])

    # if the user submits the bid form without entering any amounts, return
    if not bid:
        return redirect(productpage, product_title=product.title)

    # get the info of the product:
    product = Product.objects.get(title=product_title)

    # check that the bid is higher than the last bid
    # and that it's not the first bid (as the default for current_bid is 0)
    if product.current_bid != 0:
        if bid <= product.current_bid:
            return redirect(productpage, product_title=product.title, message="yes")
    else:
        if bid < product.price:
            return redirect(productpage, product_title=product.title, message="yes")

    # if the bid is valid (>current_bid):

    # get the info of the user:
    userinfo = User.objects.get(username=request.user)

    # update current_bid on the table Product
    product.current_bid = bid
    product.save()

    # update the table Bids
    newbid = Bid(user_id=userinfo, product_id=product, bid=bid)
    newbid.save()

    # return the user to the page of the product
    return redirect(productpage, product_title=product.title)


# Load a list of the user's Watchlist
@login_required
def watchlist(request):

    # get the info of the user:
    userinfo = User.objects.get(username=request.user)

    # get the products the user has on their watchlist
    prods = userinfo.watchedby.all().order_by('title')

    
    # render the template
    return render(request, "auctions/watchlist.html", {
        "prods": prods
    })


# load a list of all the categories
def categories(request, category=""):

    if category:

        category = Category.objects.get(category=category)
    
        products = Product.objects.filter(category=category.id, status=True)

        return render(request, "auctions/categories.html", {
            "products": products,
            "category": category
        })

    else:

        categories = Category.objects.all().order_by('category')

        return render(request, "auctions/categories.html", {
            "categories": categories
        })


# add comments to a product
@login_required
def comments(request, product_title):

    if request.method == "POST":

        # get the comments from the form:
        comment = request.POST["comment"]

        # get the info of the user:
        userinfo = User.objects.get(username=request.user)

        # get the info of the product's page the user was in:
        product = Product.objects.get(title=product_title)

        # add the comment to the table Comments
        newcomment = Comment(user_id=userinfo, product_id=product, comment=comment)
        newcomment.save()

        return redirect(productpage, product_title=product.title)


# view to create a listing
@login_required
def newlisting(request):

    # if the user got here by submitting the form
    if request.method == "POST":

        # get the info of the form
        form = CreateForm(request.POST)

        if form.is_valid():

            # process the form
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            price = int(form.cleaned_data["price"])

            # get the info on categories from the form
            categoryraw = request.POST["category"]
            category = Category.objects.get(category=categoryraw)

            # get the info of the user
            userinfo = User.objects.get(username=request.user)

            # save the new listing
            newlisting = Product(title=title, description=description, image=image, price=price, user_id=userinfo, category=category)
            newlisting.save()

            return HttpResponseRedirect(reverse("index"))


        # if the form is NOT valid, return the user to the newpage with the form filled in:
        else:
            return render(request, "auctions/createlisting.html", {
                "form": form
            })

    # if the user clicked on "create listing" to submit an item
    else:

        # collect the existing categories
        categories = Category.objects.all().order_by('category')

        # render the template with the form
        return render(request, "auctions/createlisting.html", {
            "categories": categories,
            "form": CreateForm()
        })