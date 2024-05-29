import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Post, User


def index(request):
    return render(request, "network/index.html")


@csrf_exempt
def posts(request):
    if request.user.pk:
        user = User.objects.get(pk=request.user.pk)
    page_id = request.GET.get("page_id")

    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(pk=page_id)

        if data.get("content") is not None:
            if request.user.pk != post.user.pk:
                return HttpResponse(status=403)
            post.content = data["content"]
        if data.get("like") is not None:
            if data["like"]:
                post.likes.add(request.user.pk)
            else:
                post.likes.remove(request.user.pk)
        post.save()

        return HttpResponse(status=200)

    if request.method == "POST":
        data = json.loads(request.body)
        Post(user=user, content=data["content"]).save()

        return HttpResponse(status=200)

    if page_id is not None:
        post = Post.objects.get(pk=page_id)
        return JsonResponse(post.serialize(), status=200, safe=False)

    posts = Post.objects.order_by("-timestamp").all()

    if request.GET.get("list_by") is not None:
        if request.GET.get("user_name") is not None:
            user_profile = User.objects.get(username=request.GET.get("user_name"))
            posts = posts.filter(user_id=user_profile.pk)
        else:
            following_ids = user.following.all().values_list("id", flat=True)
            posts = posts.filter(user_id__in=following_ids)

    new_posts = []
    for post in posts:
        try:
            user.liked_posts.get(pk=post.pk)
            has_user_liked = True
        except:
            has_user_liked = False

        new_posts.append(
            {
                **post.serialize(),
                "has_user_liked": has_user_liked,
                "is_user_owner": request.user.pk == post.user.pk,
            }
        )

    paginator = Paginator(new_posts, 10)
    page_number = int(request.GET.get("page"))
    page_obj = paginator.get_page(page_number)

    return JsonResponse(
        {
            "posts": page_obj.object_list,
            "current": page_obj.number,
            "next": page_obj.next_page_number() if page_obj.has_next() else None,
            "previous": (
                page_obj.previous_page_number() if page_obj.has_previous() else None
            ),
        },
        status=200,
        safe=False,
    )


@login_required
def following(request):
    return render(request, "network/index.html")


def profile(request, user_name):
    return render(request, "network/profile.html")


@csrf_exempt
def user(request, user_name):
    try:
        logged_user = User.objects.get(pk=request.user.pk)
    except:
        logged_user = False

    if request.method == "PUT":
        data = json.loads(request.body)
        user = User.objects.get(username=user_name)

        if data.get("follow"):
            logged_user.following.add(user)
        else:
            logged_user.following.remove(user)
        logged_user.save()

    if user_name is not None:
        user = User.objects.get(username=user_name)
        if logged_user:
            logged_user = True if logged_user.following.filter(id=user.pk) else False

        return JsonResponse(
            {
                **user.serialize(),
                "is_user_following": logged_user,
            },
            status=200,
            safe=False,
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
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
