from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)
router.register('likes', views.LikeViewSet)
router.register('saved', views.SavedViewSet)
router.register('tags', views.TagViewSet)

urlpatterns = [
    
    path('', include(router.urls)),  
]