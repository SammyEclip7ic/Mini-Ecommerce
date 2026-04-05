from rest_framework import serializers
from .models import Message
from apps.accounts.models import User


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    sender_name = serializers.CharField(source='sender.fullName', read_only=True)
    receiver_email = serializers.EmailField(source='receiver.email', read_only=True)
    receiver_name = serializers.CharField(source='receiver.fullName', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_email', 'sender_name',
            'receiver', 'receiver_email', 'receiver_name',
            'message', 'timestamp'
        ]
        read_only_fields = ['id', 'sender', 'timestamp']

    def validate_receiver(self, value):
        """
        Ensure receiver is not the same as sender.
        """
        request = self.context.get('request')
        if request and request.user == value:
            raise serializers.ValidationError("You cannot send a message to yourself")
        return value