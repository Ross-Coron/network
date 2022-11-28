from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Import all models
from .models import *


def index(request):
    return render(request, "network/index.html")


# Write Tweet
def tweet(request):

    if request.method == "POST":
        form_contents = request.POST["exampleFormControlTextarea1"]
        print(form_contents)

        newTweet = Tweet(author=request.user, tweetText=form_contents)
        newTweet.save()

        return HttpResponseRedirect(reverse("allPosts"))

    else:
        return render(request, "network/tweet.html")


# View all Tweets
def allPosts(request):

    tweets = Tweet.objects.all()
    print(tweets)

    return render(request, "network/allPosts.html", {
        "tweets": tweets
    })


# View user profile and their Tweets
def profile(request):

    # Returns in reverse chronolical order
    tweets = Tweet.objects.filter(author=request.user).order_by('-posted')
    
    return render(request, "network/profile.html", {
        "tweets": tweets,
        "following": request.user.foo.all().count(),
        "followedBy": Follow.objects.filter(user=request.user).count()
    })


# Log in, out, register

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
