from django.template.context_processors import request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticated

from .filters import UserMessagesFilterBackend
from .models import Message
from .serializers import MessageSerializer

class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()

    filter_backends = [UserMessagesFilterBackend, DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['receiver']
    search_fields = ['body']

class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
