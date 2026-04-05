from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    """
    List messages for authenticated user or create a new message.
    GET: Returns messages where user is sender or receiver
    POST: Create a new message
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return messages where the user is either sender or receiver.
        """
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver').order_by('-timestamp')

    def perform_create(self, serializer):
        """
        Set the sender to the authenticated user.
        """
        serializer.save(sender=self.request.user)