from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostsListAPIView.as_view(), name='posts'),
    path('<int:id>', views.PostDetailAPIView.as_view(), name='posts')
]