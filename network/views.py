from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# from mail
import json
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

# From Mail. 
from django.http import JsonResponse

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


# View a user's profile and their Tweets
def profile(request, user_id):

    # BETTER
    profile = User.objects.get(id=user_id)
    if Follow.objects.filter(user=user_id, followed_by=request.user).exists():
        print("ya")
        following_status = True
    else:
        print("na")
        following_status = False
   
    # Get list of IDs of people the logged in user follows (Follow objects)
    followList = []
    following = request.user.following.all()
    for x in following:
        followList.append(x.user.id)

    # Get user of profile being viewed (User object)
    profile = User.objects.get(id=user_id)
    
    
    if profile.id in followList:
        print("You are following")
    else:
        print("You are NOT following")

    
    # Returns in reverse chronolical order
    tweets = Tweet.objects.filter(author=user_id).order_by('-posted')
    print(tweets)


    return render(request, "network/profile.html", {
        "x": profile.username,
        "tweets": tweets,
        "following": profile.following.all().count(),
        "followedBy": Follow.objects.filter(user=user_id).count(),
        "following_status": following_status
    })


def following(request):

 
    # Gets all users following logged in user
    usersFollowed = request.user.following.all()
  
    # Gets IDs of users to filter with
    usersFollowedIds = []
    for x in usersFollowed:
        usersFollowedIds.append(x.user.id)

    print(usersFollowedIds)
    
    #Filter Tweets by list of IDs
    tweets = Tweet.objects.filter(author__in=usersFollowedIds).order_by('-posted')
    
    return render(request, "network/allPosts.html", {
        "tweets": tweets
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


# Currently here. API route to follow / unfollow user.
def test(request, user_id):
    
    print(user_id)

    print("Current user:", request.user.id)
    
    # Temp
    following = User.objects.get(id=request.user.id).following.filter(user=3).get()


    profile = User.objects.get(id=request.user.id)

    profile.following.remove(following)


    print(following.user)

    #follow = User.objects.filter(username=request.user).following
    

    return JsonResponse({"message": "Success!"}, status=201)


@csrf_exempt
def edit(request, post_id):

    print("You are here")
    print(post_id)

    print(json.loads(request.body))

    tweet = Tweet.objects.get(pk=post_id)

    data = json.loads(request.body)
    new_text = data.get("tweet", "t")
    print(tweet)


    tweet.tweetText = new_text
    tweet.save()

    print(tweet)

    return JsonResponse({"message": "Tweet successfully edited", "new_text": new_text}, status=201)


@csrf_exempt
def like(request, post_id):

    print("You are here 2")
    print(post_id)

 #   data = json.loads(request.body)
 #   print(data)

  #  status = data.get('like')
  #  print(status)
  #  print(type(status))

    

    user = User.objects.get(id=request.user.id)
    tweet = Tweet.objects.get(id=post_id)

    
    
    if user in tweet.like.all():
        print("yes")
    else:
        print("no")

    return JsonResponse({"message": "Like function"})
