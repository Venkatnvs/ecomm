from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .chat_responce_v4 import ChatbotLogic
from store.models import Product
from django.template.loader import get_template

def index(request):
    return render(request, 'chatapp/index.html')

def room(request, room_name):
    context = {
        'room_name': room_name
    }
    return render(request, 'chatapp/room.html', context)

# @login_required()
def ChatBotIndex(request):
    return render(request, 'chatapp/chatbot_fullpg/index.html')

@api_view(['GET','POST'])
def chatbot_api(request):
    user_message = request.data.get('message', '')
    user_message = user_message.lower()
    chatbot_logic = ChatbotLogic(request)
    bot_response = chatbot_logic.process_user_message(user_message)
    return Response({'response': bot_response})

@api_view(['GET'])
def test_snippets(request):
    products = Product.objects.all().reverse()[0:5]
    context = {
        "products":products,
        "heading":"Top 5 Products:"
    }
    products_info = get_template("chatapp/chatbot_fullpg/ans_snippets/all_products.html").render(context)
    return Response({"responce":products_info})

def test_snippets2(request):
    return render(request,"chatapp/chatbot_fullpg/test_ans.html")