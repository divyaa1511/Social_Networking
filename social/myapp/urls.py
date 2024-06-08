from django.db import models

# Create your models here.
from django.urls import path
from .views import UserLogin, UserSignup, SendFriendRequest, AcceptFriendRequest, RejectFriendRequest, ListFriends, ListPendingFriendRequests, SearchUsers

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('signup/', UserSignup.as_view(), name='signup'),
    path('send-friend-request/', SendFriendRequest.as_view(), name='send_friend_request'),
    path('accept-friend-request/', AcceptFriendRequest.as_view(), name='accept_friend_request'),
    path('reject-friend-request/', RejectFriendRequest.as_view(), name='reject_friend_request'),
    path('list-friends/', ListFriends.as_view(), name='list_friends'),
    path('list-pending-friend-requests/', ListPendingFriendRequests.as_view(), name='list_pending_friend_requests'),
    path('search-users/', SearchUsers.as_view(), name='search_users'),
]
