import json
import time
from cent import Client, PublishRequest
from django.conf import settings
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Prefetch
from django.core.cache import cache
import jwt
import requests

from sem7.models import Chat, Message, UserInChat


def heavy_lifting():
    response = requests.get(
        "https://api.api-ninjas.com/v2/randomquotes",
        headers={"X-Api-Key": settings.API_KEY}
    )

    if response.status_code == 200:
        quote = response.json()[0]["quote"]
        return quote


def get_cached_heavy_lifting():
    CACHE_KEY = "quote"
    quote = cache.get(CACHE_KEY)
    if not quote:
        quote = heavy_lifting()
        cache.set(CACHE_KEY, quote, timeout=5)
    return quote


def generate_token(user_id):
    token = jwt.encode({
        "sub": str(user_id),
        "exp": int(time.time() * 10 * 60),
    }, settings.CENTRIFUGO_HMAC_SECRET, algorithm="HS256")
    return token


def publish_to_centrifuge(channel, data):
    api_url = f"http://{settings.CENTRIFUGO_URL}/api"
    client = Client(api_url, settings.CENTRIFUGO_API_KEY)
    request = PublishRequest(channel=channel, data=data)
    client.publish(request)


class IndexView(TemplateView):
    template_name = "sem7/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users_prefetch = Prefetch(
            "users_in_chats", to_attr="users",
            queryset=UserInChat.objects.exclude(user_id=self.request.user.pk).select_related("user")
        )
        messages_prefetch = Prefetch(
            "messages", to_attr="last_messages",
            queryset=Message.objects.order_by("-created_at").select_related("author")[:10]
        )
        context["chats"] = Chat.objects \
            .prefetch_related(users_prefetch, messages_prefetch) \
            .filter(users_in_chats__user_id=self.request.user.pk)

        token = generate_token(self.request.user.pk)
        context["centrifuge_token"] = token
        context["centrifuge_url"] = settings.CENTRIFUGO_URL
        context["quote"] = get_cached_heavy_lifting()
        return context


class ChatView(TemplateView):
    template_name = "sem7/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        users_prefetch = Prefetch(
            "users_in_chats", to_attr="users",
            queryset=UserInChat.objects.exclude(user_id=self.request.user.pk).select_related("user")
        )

        messages_prefetch = Prefetch(
            "messages", to_attr="last_messages",
            queryset=Message.objects.order_by("-created_at").select_related("author")[:10]
        )

        chat = Chat.objects \
            .prefetch_related(users_prefetch, messages_prefetch) \
            .filter(id=kwargs["chat_pk"], users_in_chats__user_id=self.request.user.pk) \
            .first()

        if not chat:
            raise Http404()

        token = generate_token(self.request.user.pk)
        context["centrifuge_token"] = token
        context["centrifuge_url"] = settings.CENTRIFUGO_URL
        context["centrifuge_channel"] = f"chat_{chat.id}"
        context["chat"] = chat
        return context


class CreateMessageView(View):
    http_method_names = ["post"]

    def post(self, request, chat_pk, *args, **kwargs):
        # !! Очень небезопасно, пожалуйста не делайте так !!
        data = json.loads(request.body)
        message = Message.objects.create(chat_id=chat_pk, author_id=request.user.pk, text=data["text"])

        serialized_message = {
            "id": message.id,
            "text": message.text,
            "author": {"id": request.user.pk, "email": request.user.email},
            "created_at": message.created_at.strftime("%H:%M")
        }
        channel = f"chat_{chat_pk}"
        publish_to_centrifuge(channel, {"message": serialized_message})

        return JsonResponse({}, status=200)
