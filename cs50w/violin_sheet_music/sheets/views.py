import json
import math
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from sheets.forms import AttemptForm, SheetForm
from sheets.models import Attempt, Sheet

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse

from .models import User


NUMBER_OF_PAGES = 3


# Create your views here.
def index(request):
    return render(request, "sheets/index.html")


@login_required
def upload_sheet(request):
    if request.method == "POST":
        form = SheetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            return render(
                request,
                "sheets/upload.html",
                {"form": SheetForm(), "error": form.errors.as_text},
            )
    return render(request, "sheets/upload.html", {"form": SheetForm()})


@csrf_exempt
def sheets(request):
    search = request.GET.get("search")
    if search:
        sheets = Sheet.objects.filter(name__contains=search).order_by("-timestamp")
    else:
        sheets = Sheet.objects.order_by("-timestamp")

    paginator = Paginator([sheet.serialize() for sheet in sheets], NUMBER_OF_PAGES)
    page_number = int(request.GET.get("page"))
    page_obj = paginator.get_page(page_number)

    return JsonResponse(
        {
            "results": page_obj.object_list,
            "count": math.ceil(len(sheets.all()) / NUMBER_OF_PAGES),
            "current": page_obj.number,
            "next": page_obj.next_page_number() if page_obj.has_next() else None,
            "previous": (
                page_obj.previous_page_number() if page_obj.has_previous() else None
            ),
        },
        status=200,
    )


@csrf_exempt
def sheet(request, id):
    sheet = Sheet.objects.get(pk=id)
    attempts = Attempt.objects.filter(sheet=id).order_by("-rating")
    order_by = request.GET.get("order_by")

    if order_by == "date":
        attempts = attempts.order_by("-timestamp")
    if order_by == "rating":
        attempts = attempts.order_by("-rating")

    attempts_data = []
    for attempt in attempts:
        try:
            attempt.ratings.get(pk=request.user.pk)
            user_rated = True
        except:
            user_rated = False

        attempts_data.append(
            {
                **attempt.serialize(),
                "ratings": attempt.ratings.all(),
                "user_rated": user_rated,
            }
        )

    return render(
        request,
        "sheets/sheet.html",
        {
            "form": AttemptForm(),
            "sheet": sheet,
            "attempts": attempts_data,
            "error": request.GET.get("error", ""),
        },
    )


@login_required
def attempt(request, id):
    sheet = Sheet.objects.get(pk=id)

    if request.method == "POST":
        form = AttemptForm(request.POST, request.FILES)
        if form.is_valid():
            attempt = form.save(commit=False)
            attempt.user = request.user
            attempt.save()
            attempt.sheet.add(sheet)
            form.save_m2m()
        else:
            return HttpResponseRedirect(f"/sheet/{id}?error={form.errors.as_text}")
    return HttpResponseRedirect(f"/sheet/{id}")


@csrf_exempt
@login_required
def rate(request, attempt_id):
    if request.method == "PUT":
        attempt = Attempt.objects.get(pk=attempt_id)
        rating = json.loads(request.body).get("rating")
        if rating is not None:
            attempt.ratings.add(request.user.pk)
            attempt.rating = int(
                (attempt.rating + rating) / (len(attempt.ratings.all()))
            )
            attempt.save()
        else:
            return HttpResponse(status=400)
    return HttpResponse(status=200)


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
                "sheets/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "sheets/login.html")


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
                request, "sheets/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "sheets/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sheets/register.html")
