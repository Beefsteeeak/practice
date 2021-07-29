from django.urls import path

from . import views
from .views import PostListView, UserPublicProfile

app_name = 'blog'
urlpatterns = [
    path('post/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/create/', views.post_creation, name='post-create'),
    path('post/user/', views.post_user_list, name='user-post-list'),
    path('post/contact/', views.contact, name='contact'),

    path('profile/<int:pk>', UserPublicProfile.as_view(), name='user-public-profile'),
]
