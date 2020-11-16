from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .form import MerchandiseForm
from .models import Merchandise
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='login')
def index(request):
    merchandise = Merchandise.objects.all().order_by('-acquisition_date')
    print(merchandise)
    return render(request, "capstone/index.html", {"merchandise": merchandise})

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
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")


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
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")

@login_required(login_url='login')
def addMerchandise(request):
    if request.method == "POST":
        merchandise = MerchandiseForm(request.POST, instance=Merchandise(user = request.user))
        if merchandise.is_valid():
            try:
                merchandise.save()
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError as e:
                return render(request, "capstone/addMerchandise.html", { 
                    "message": "Code already exists",
                    "merchandise_form": merchandise
                })
    else:
        merchandise = MerchandiseForm()
    
    return render(request, "capstone/addMerchandise.html", {"merchandise_form": merchandise})

def showMerchandise(request, code):
    merchandise = Merchandise.objects.get(user=request.user, code=code)
    return render(request, "capstone/showMerchandise.html", {"merchandise": merchandise.serialize()})



# API METHODS!!!

@csrf_exempt
@login_required
def getMerchandise(request, merchandise_id):
    # Query for requested merchandise
    try:
        merchandise = Merchandise.objects.get(user=request.user, pk=merchandise_id)
    except Merchandies.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post content
    if request.method == "GET":
        return JsonResponse(merchandise.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            merchandise.content = data["content"]
        merchandise.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
