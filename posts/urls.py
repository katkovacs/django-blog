from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='all'),
    path('new/', views.CreatePost.as_view(), name='create'),
    path('by/<slug:slug>', views.UserPosts.as_view(), name='for_user'),
    path('by/<slug:slug>/<int:pk>/', views.PostDetail.as_view(), name='single'),
    path('delete/<int:pk>/', views.DeletePost.as_view(), name='delete'),
    path('<int:pk>/like/', views.LikeView.as_view(), name='like'),
    path('<int:pk>/unlike/', views.UnlikeView.as_view(), name='unlike'),
    path('<slug:slug>/likes', views.UserLikesPostsList.as_view(), name='user_likes'),
]