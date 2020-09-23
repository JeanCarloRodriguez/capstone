from django.shortcuts import render
def index(request):
    return render(request, "capstone/index.html")

def login(request):
    return render(request, "capstone/login.html")

def register(request):
    pass