from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Conversation
from .serializers import ConversationListSerializer, ConversationDetailSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversations_list(request):
    # Get user's actual conversations
    user_conversations = request.user.conversations.all()
    
    # If no conversations exist, create a sample conversation for demonstration
    if not user_conversations.exists():
        from django.utils import timezone
        from .models import ConversationMessage
        from useraccount.models import User
        
        # Create a sample conversation with the current user and another user
        other_users = User.objects.exclude(id=request.user.id)
        if other_users.exists():
            other_user = other_users.first()
        else:
            # If no other users exist, use the same user (for testing purposes)
            other_user = request.user
        
        sample_conversation = Conversation.objects.create()
        sample_conversation.users.add(request.user, other_user)
        
        # Add sample messages that match the ConversationDetail component
        ConversationMessage.objects.create(
            conversation=sample_conversation,
            created_by=other_user,
            body="Hello this is me",
            sent_to=request.user
        )
        ConversationMessage.objects.create(
            conversation=sample_conversation,
            created_by=request.user,
            body="Hello this is me",
            sent_to=other_user
        )
        
        # Refresh the queryset
        user_conversations = request.user.conversations.all()
    
    serializer = ConversationListSerializer(user_conversations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_detail(request, pk):
    try:
        conversation = request.user.conversations.get(pk=pk)
        serializer = ConversationDetailSerializer(conversation, many=False)
        return Response(serializer.data)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
