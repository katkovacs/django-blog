from django.urls import path

from . import views
from posts.views import UserPosts

app_name = 'user_profile'

urlpatterns = [
    # path('find', views.PostList.as_view(), name='find'),
    # path('bla/', views.ShowProfile.as_view(), name='profile'),
    path('', views.ProfileDetail.as_view(), name='profile_detail'),
    path('posts/', UserPosts.as_view(), name='myposts'),
    path('update-profile/', views.UserProfileUpdateView.as_view(), name='edit_profile'),
    path('people', views.ProfileListAll.as_view(), name='people'),
    path('following', views.ProfileListFollowing.as_view(), name='following'),
    path('followers', views.ProfileListFollowers.as_view(), name='followers'),
    path('follow', views.FollowView.as_view(), name='follow'),
    path('unfollow', views.UnfollowView.as_view(), name='unfollow'),
]
