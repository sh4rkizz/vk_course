from django.urls import path
from sem7.views import ChatView, CreateMessageView, IndexView

app_name = "sem7"

urlpatterns = [
    path('', IndexView.as_view(), name="index_page"),
    path('chat/<int:chat_pk>/', ChatView.as_view(), name="chat_page"),
    path('chat/<int:chat_pk>/messages/', CreateMessageView.as_view(), name="create_message")
]
