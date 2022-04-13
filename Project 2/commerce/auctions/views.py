from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from requests import RequestException
from django.contrib.auth.decorators import login_required
from .models import Listing, User


def index(request):
    products = Listing.objects.all()
    return render(
            request,
            "auctions/index.html",
            {"products": products},
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def createlisting(request):
    if request.method == "POST":
        item = Listing()
        item.seller = request.user.username
        item.title = request.POST.get("title")
        item.description = request.POST.get("description")
        item.category = request.POST.get("category")
        item.starting_bid = request.POST.get("starting_bid")
        item.image_link = request.POST.get("image_link")
        item.save()
        products = Listing.objects.all()
        if len(products) == 0:
            empty = True
        else:
            empty = False
        print(item)
        return render(
            request,
            "auctions/index.html",
            {"products": products, "empty": empty},
        )
    else:
        return render(request, "auctions/createlisting.html")
