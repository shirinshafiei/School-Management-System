from django.urls import path
from .views import MessageListAPIView, MessageCreateAPIView

urlpatterns = [
    path('messages/', MessageListAPIView.as_view(), name='message-list'),
    path('messages/send/', MessageCreateAPIView.as_view(), name='message-create'),
]
