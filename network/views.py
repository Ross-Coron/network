from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator   # Pagination functionality   
import json # JSON functionality
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt   # CSRF exemption
from .models import *   # Import all models


# Index route (default)
def index(request):

    if request.user.is_authenticated:
        return render(request, "network/index.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
    

# Create new post
@login_required(redirect_field_name='my_redirect_field')   # Redirect to login. Route saved in settings.py
def tweet(request):

    if request.method == "POST":
        
        # Get content of textarea
        form_contents = request.POST["exampleFormControlTextarea1"]
        # print("Debug | post text:", form_contents)

        # Add post to database
        newTweet = Tweet(author=request.user, tweetText=form_contents)
        newTweet.save()

        # Redirect to all posts page
        return HttpResponseRedirect(reverse("allPosts"))

    else:
        return render(request, "network/tweet.html")


# View all posts
@login_required(redirect_field_name='my_redirect_field')
def allPosts(request):

    # Get all posts and paginate (10 posts per page)
    tweets = Tweet.objects.all().order_by('-posted')
    paginator = Paginator(tweets, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # print("Debug | all tweets:",tweets)

    return render(request, "network/allPosts.html", {
        "page_obj": page_obj
    })


# View user profile and their posts
@login_required(redirect_field_name='my_redirect_field')
def profile(request, user_id):

    # Get profile
    profile = User.objects.get(id=user_id)

    # Check if user follows profile
    if Follow.objects.filter(user=user_id, followed_by=request.user).exists():
        # print("Debug | user is following profile")
        following_status = True
    else:
        # print("Debug | user is NOT following profile")
        following_status = False
   
    # Get list of IDs of people the logged in user follows (Follow objects)
    followList = []
    following = request.user.following.all()
    for x in following:
        followList.append(x.user.id)
    
    # Gets posts from profile in reverse chronological order
    tweets = Tweet.objects.filter(author=user_id).order_by('-posted')
    # print("Debug | profile's posts: ",tweets)

    paginator = Paginator(tweets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "viewed_profile": profile.username,
        "viewed_profile_id": user_id,
        "tweets": tweets,
        "following": profile.following.all().count(),
        "followedBy": Follow.objects.filter(user=user_id).count(),
        "following_status": following_status
    })


# Displays posts from profiles user is following
@login_required(redirect_field_name='my_redirect_field')
def following(request):

    # Gets all profiles user follows
    usersFollowed = request.user.following.all()
  
    # Make list of IDs
    usersFollowedIds = []
    for x in usersFollowed:
        usersFollowedIds.append(x.user.id)

    # print("Debug | User follows: ", usersFollowedIds)
    
    # Gets posts from profiles in reverse chronological order
    tweets = Tweet.objects.filter(author__in=usersFollowedIds).order_by('-posted')
    
    paginator = Paginator(tweets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


# Log user in
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


# Log user out
@login_required(redirect_field_name='my_redirect_field')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register a new user
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


# API function: follow / unfollow profile
@login_required(redirect_field_name='my_redirect_field')
def follow(request, user_id):
    
    # Get user 
    user = User.objects.get(pk=request.user.id)
    print("Debug:", user, type(user), user.following.all())
    
    # Get profile being viewed
    profile = User.objects.get(pk=user_id)
    print("Debug:", profile, type(profile), profile.following.all())

    # Check if user already follows profile. If so, remove
    if Follow.objects.filter(user=profile, followed_by=user).exists():        
      
        print("Debug: user currently following profile")
        instance = Follow.objects.filter(user=profile, followed_by=user).get()

        user.following.remove(instance)

        # If empty ManyToMany field, delete relationship
        a = Follow.objects.filter(user=profile)
        for x in a:
            if not x.followed_by.exists():
                x.delete()

        print("Debug: user no longer following profile")

    else:
        
        print("Debug: user NOT currently following profile")
        instance = Follow(user=profile)
        instance.save()

        instance.followed_by.add(user)
        print("Debug: user now following profile")

    return JsonResponse({"message": "Profile successfully followed / unfollowed"}, status=201)


# API function: Edit post
@csrf_exempt
@login_required(redirect_field_name='my_redirect_field')
def edit(request, post_id):

    # print("Debug | Edit function, post: ", post_id)
 
    # Get original post
    tweet = Tweet.objects.get(pk=post_id)

    # Gets new text (edited) in JSON format
    data = json.loads(request.body)
    new_text = data.get("tweet", "t")
    
    # Update post to new text
    tweet.tweetText = new_text
    tweet.save()

    # Return new text for instant display
    return JsonResponse({"message": "Post successfully edited", "new_text": new_text}, status=201)


# API function: Like post
@csrf_exempt
@login_required(redirect_field_name='my_redirect_field')
def like(request, post_id):

    # Debug: print("Debug | Like function")

    # Get user and relevant post
    user = User.objects.get(id=request.user.id)
    tweet = Tweet.objects.get(id=post_id)

    # If user likes post unlike (and vice versa)
    if user in tweet.like.all():
        print("Debug | User already likes this post - unliking now")
        tweet.like.remove(user)

    else:
        print("Debug: user does not yet like this post - liking now")
        tweet.like.add(user)

    return JsonResponse({"message": "Post successfully liked / disliked"})