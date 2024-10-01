from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChatHistory

@csrf_exempt
def index(request):
    global chat_history
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            chat_history = ChatHistory.objects.get(pk=2)
            if data.get('prompt').split("~")[0] == "start_message_for_the_service ":
                chat_history.chat_history += f"\nUser: {data.get('prompt').split('~')[-1]}\n"
                chat_history.chat_history += "ChatBot: "
            else:
                chat_history.chat_history += f"\nUser: {data.get('prompt')}\n"
                chat_history.chat_history += "ChatBot: "
            
            payload = {
                "model": data.get("model"),
                "prompt": chat_history.chat_history,
            }

            api_url = "http://localhost:11434/api/generate"

            response = requests.post(api_url, json=payload)

            response_ = ""

            for line in response.text.splitlines():
                try:
                    json_data = json.loads(line)
                    response_ += json_data["response"]
                except json.JSONDecodeError:
                    print("Non-JSON line:", line)

            chat_history.chat_history += response_
            chat_history.save()

            return HttpResponse(response_)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)
    return HttpResponse("Forbidden", status=403)