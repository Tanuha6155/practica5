from django.urls import path
from .views import Posts, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,


urlpatterns = [
    path('', Posts.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'), # Ссылка на детали товара
    path('create/', PostCreateView.as_view(), name='post_create'), # Ссылка на создание товара
]
