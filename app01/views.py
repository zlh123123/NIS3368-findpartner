from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "home/home.html")

def login(request):
    return render(request, "home/login.html")

def mainpage(request):
    context = {
        "user": request.user,
    }
    return render(request, "mainpage/mainpage.html", context)

def main(request):
    return render(request, "mainpage/main.html")

def publish(request):
    return render(request, "user/push.html")
