from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from .models import CustomUser, FriendRequest
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


# User Registration

class UserSignup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create_user(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
                password=request.data['password']
            )
            user.date_joined = timezone.now()
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            print(user)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Send Friend Request

class SendFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')

        try:
            receiver = CustomUser.objects.get(id=receiver_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Receiver not found.'}, status=status.HTTP_404_NOT_FOUND)

        if FriendRequest.objects.filter(sender=sender, receiver=receiver, status='pending').exists():
            return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(sender=sender, created_at__gte=one_minute_ago).count()
        if recent_requests_count >= 3:
            return Response({'error': 'You can only send 3 friend requests per minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        FriendRequest.objects.create(sender=sender, receiver=receiver)
        return Response({'message': 'Friend request sent successfully.'}, status=status.HTTP_201_CREATED)

# Accept Friend Request

class AcceptFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver = request.user
        sender_id = request.data.get('sender_id')

        try:
            sender = CustomUser.objects.get(id=sender_id)
            print('hi')
        except CustomUser.DoesNotExist:
            return Response({'error': 'Sender not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if friend request exists
        friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, status='pending').first()
        if not friend_request:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
        friend_request.status = 'accepted'
        friend_request.save()
        return Response({'message': 'Friend request accepted successfully.'}, status=status.HTTP_200_OK)

# Reject Friend Request

class RejectFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver = request.user
        sender_id = request.data.get('sender_id')
        print(f"Receiver: {receiver.email}, Sender ID: {sender_id}")

        try:
            sender = CustomUser.objects.get(id=sender_id)
            print(f"Sender found: {sender.id}")
        except CustomUser.DoesNotExist:
            print("Sender not found.")
            return Response({'error': 'Sender not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if friend request exists
        friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, status='pending').first()
        if not friend_request:
            print("Friend request not found.")
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Reject friend request
        friend_request.status = 'rejected'
        friend_request.save()
        print("Friend request rejected successfully.")
        return Response({'message': 'Friend request rejected successfully.'}, status=status.HTTP_200_OK)
    
# List of all friends

class ListFriends(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        sent_requests = FriendRequest.objects.filter(sender=user, status='accepted').values_list('receiver', flat=True)
        received_requests = FriendRequest.objects.filter(receiver=user, status='accepted').values_list('sender', flat=True)

        friends_ids = set(sent_requests).union(set(received_requests))
        friends = CustomUser.objects.filter(id__in=friends_ids)

        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# List of Pending Friend Requests

class ListPendingFriendRequests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get all pending friend requests where the user is the receiver
        pending_requests = FriendRequest.objects.filter(receiver=user, status='pending')
        senders = [req.sender for req in pending_requests]

        serializer = UserSerializer(senders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Search User by email or by username

class CustomPagination(PageNumberPagination):
    page_size = 10

class SearchUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '')
        print("q",query)
        if query:
            print("hi")
            # Search by email or name
            users = CustomUser.objects.filter(
                Q(email__iexact=query) | Q(username__icontains=query)
            )
        else:
            users = CustomUser.objects.none()

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)