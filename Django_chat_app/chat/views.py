from django.shortcuts import render, redirect
from .models import Chat, Message
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


@login_required(login_url="/login/")
def index(request):
    if request.method == "POST":
        print("Received data " + request.POST["textmessage"])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(
            text=request.POST["textmessage"],
            chat=myChat,
            author=request.user,
            receiver=request.user,
        )
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, "chat/index.html", {"messages": chatMessages})


def login_view(request):
    redirect_url = request.GET.get("next")
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )

        if user:
            login(request, user)
            return redirect(redirect_url or 'index')  # Weiterleitung zum nächsten Ziel oder zur Chat-Seite
        else:
            return render(request, "auth/login.html", {"wrongPassword": True, 'redirect': redirect_url})

    return render(request, "auth/login.html", {'redirect': redirect_url})

def registration_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Überprüfen, ob die E-Mail-Adresse bereits verwendet wird
        if User.objects.filter(email=email).exists():
            messages.error(request, "Diese E-Mail-Adresse wird bereits verwendet.")
            return render(request, "auth/registration.html")

        # Neuen Benutzer erstellen
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Registrierung erfolgreich! Sie können sich jetzt anmelden.")
        return redirect('login_view')  # Weiterleitung zur Login-Seite nach erfolgreicher Registrierung

    return render(request, "auth/registration.html")