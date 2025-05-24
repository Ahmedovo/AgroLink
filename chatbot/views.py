from django.shortcuts import render
from django.http import JsonResponse
from .utils import train_bot, get_bot_response

# Ensure the model is trained on startup
train_bot()

def chatbot_home(request):
    return render(request, 'chatbot/chatbot.html')

def chatbot_response(request):
    user_message = request.GET.get('message', '')
    reply = get_bot_response(user_message)
    return JsonResponse({'reply': reply})
