from django.shortcuts import render
from .models import Message, Chat
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print("Received data" + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        new_Message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [new_Message])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1) # chat__id=1 > Man schaut von der Message auf das Objekt Chat mit der id 1
    return render(request, 'chat/index.html', {'messages': chatMessages})

def loginView(request):
    wrongPassword = False
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            serialized_obj = serializers.serialize('json', [user])
            return JsonResponse(serialized_obj[1:-1], safe=False)
            
    return render(request, 'auth/login.html')    

def signUpView(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        print(user)
        print(username)
        print(User.objects.get(username=username))

        try:
            User.objects.get(username=username)
            serialized_obj = serializers.serialize('json', [user])
            return JsonResponse(serialized_obj[1:-1], safe=False)
        except:
            user.save()
            login(request, user)
            serialized_obj = serializers.serialize('json', [user])
            print(serialized_obj)
            return JsonResponse(serialized_obj[1:-1], safe=False)
        
    return render(request, 'auth/registration.html')