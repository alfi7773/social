from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from .yasg import urlpatterns as url_doc

router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)
# router.register('likes', views.LikePostView)
router.register('saved', views.SavedViewSet)
router.register('tags', views.TagViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('likes/', views.LikePostView.as_view(), name='like_post'),
    path('', include(router.urls)),  
]

urlpatterns += url_doc