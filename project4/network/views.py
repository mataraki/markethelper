import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):

    posts = Post.objects.order_by("-timestamp").all()
    serializedposts = [post.serialize() for post in posts]
    p = Paginator(serializedposts, 10)
    return render(request, "network/index.html", {
        "apipath": "/posts/",
        "followfeature": False,
        "followed": False,
        "header": "All Posts",
        "name": request.user,
        "newpost": True,
        "pagecount": p.num_pages,
        "pagenumber": 1,
        "userpage": False,
        "viewer": request.user
    })


@csrf_exempt
@login_required
def follow(request, name):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    user = User.objects.get(username = name)
    profile = User.objects.get(username = request.user)

    if len(Follow.objects.filter(follow = user).filter(follower = profile)) > 0:
        Follow.objects.filter(follow = user).filter(follower = profile).delete()
        followers = len(user.followers.all())
        status = "Follow"
    else:
        following = Follow(
            follow=user,
            follower=profile
        )
        following.save()
        followers = len(user.followers.all())
        status = "Unfollow"

    return JsonResponse({"followers": followers, "status": status}, status=201)


@csrf_exempt
@login_required
def edit(request, postid):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    editbody = json.loads(request.body)['body']

    if Post.objects.get(id = postid).user == request.user:
        Post.objects.filter(id = postid).update(body=editbody)

        return JsonResponse({"message": "Post edited succesfully."}, status=201)

    else:
        return JsonResponse({"error": "Cannot edit other person's post."}, status=400)


def following(request):

    followlist = []
    followings = User.objects.get(username = request.user).follows.all()
    for following in followings:
        followlist.append(following.follow)

    posts = Post.objects.filter(user__in = followlist).order_by("-timestamp").all()
    serializedposts = [post.serialize() for post in posts]
    p = Paginator(serializedposts, 10)

    return render(request, "network/index.html", {
        "apipath": "/following/posts/",
        "followfeature": False,
        "followed": False,
        "header": "Following",
        "name": request.user,
        "newpost": False,
        "pagecount": p.num_pages,
        "pagenumber": 1,
        "userpage": False,
        "viewer": request.user
    })


def followingposts(request, pagenumber):

    followlist = []
    followings = User.objects.get(username = request.user).follows.all()
    for following in followings:
        followlist.append(following.follow)

    posts = Post.objects.filter(user__in = followlist).order_by("-timestamp").all()
    serializedposts = [post.serialize() for post in posts]
    p = Paginator(serializedposts, 10)
    return JsonResponse({"body": p.page(pagenumber).object_list, "pagenumber": pagenumber}, safe=False)


@csrf_exempt
@login_required
def like(request, postid):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    post = Post.objects.get(id = postid)

    if request.user in post.likers.all():
        post.likers.remove(User.objects.get(username = request.user))
        post.likes = post.likes - 1
        post.save()
    else:
        post.likers.add(User.objects.get(username = request.user))
        post.likes = post.likes + 1
        post.save()

    return JsonResponse(post.serialize(), safe=False)


@csrf_exempt
@login_required
def newpost(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check if post is blank
    data = json.loads(request.body)
    if data['body'] == "":
        return JsonResponse({"error": "Blank post."}, status=400)

    # Get body of post
    body = data.get("body", "")

    # Create the post
    post = Post(
        user=request.user,
        body=body,
    )
    post.save()

    return JsonResponse({"message": "Post created succesfully."}, status=201)


def posts(request, pagenumber):

    posts = Post.objects.order_by("-timestamp").all()
    serializedposts = [post.serialize() for post in posts]
    p = Paginator(serializedposts, 10)
    return JsonResponse({"body": p.page(pagenumber).object_list, "pagenumber": pagenumber}, safe=False)


def profile(request):

    follows = len(User.objects.get(username = request.user).follows.all())
    followers = len(User.objects.get(username = request.user).followers.all())

    posts = Post.objects.filter(user = User.objects.get(username = request.user)).order_by("-timestamp").all()
    serializedposts = [post.serialize() for post in posts]
    p = Paginator(serializedposts, 10)

    return render(request, "network/index.html", {
        "apipath": f"/user/{ request.user }/posts/",
        "followfeature": False,
        "followed": False,
        "followers": followers,
        "follows": follows,
        "header": f"{ request.user }",
        "name": request.user,
        "newpost": False,
        "pagecount": p.num_pages,
        "pagenumber": 1,
        "userpage": True,
        "viewer": request.user
    })


def user(request, name):

    followed = False

    poster = User.objects.get(username = name)
    if request.user.is_authenticated:
        profile = User.objects.get(username = request.user)

        if poster == profile:
            return HttpResponseRedirect(reverse("profile"))

        if len(Follow.objects.filter(follow = poster).filter(follower = profile)) > 0:
            followed = True
        else:
            followed = False

    follows = len(poster.follows.all())
    followers = len(poster.followers.all())

    posts = Post.objects.filter(user = User.objects.get(username = name)).order_by("-timestamp").all()
    serializedposts = [post.serialize() for post in posts]
    p = Paginator(serializedposts, 10)

    return render(request, "network/index.html", {
        "apipath": f"/user/{ poster }/posts/",
        "followfeature": True,
        "followed": followed,
        "followers": followers,
        "follows": follows,
        "header": f"{ poster }",
        "name": poster,
        "newpost": False,
        "pagecount": p.num_pages,
        "pagenumber": 1,
        "userpage": True,
        "viewer": request.user
    })


def userposts(request, name, pagenumber):

    posts = Post.objects.filter(user = User.objects.get(username = name)).order_by("-timestamp").all()
    serializedposts = [post.serialize() for post in posts]
    p = Paginator(serializedposts, 10)
    return JsonResponse({"body": p.page(pagenumber).object_list, "pagenumber": pagenumber}, safe=False)


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
