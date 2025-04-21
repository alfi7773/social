from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from .yasg import urlpatterns as url_doc
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

# Ресурсы с постами
router.register('posts', views.PostViewSet)
router.register('post-comments', views.CommentViewSet)  
# router.register('post-likes', views.LikePostView)  
# router.register('post-likes', views.LikePostView, basename='likepost')
# router.register('post-saves', views.SavedItemViewSet, basename='save') 
router.register('post-images', views.PostImageViewSet)
router.register('post-tags', views.PostTagViewSet)

router.register('users', views.AllUser)
router.register('user-images', views.UserImage)
router.register('user-saves', views.SavedViewSet)
router.register('user-likes', views.PostsByUserView, basename='user-likes')
router.register('user-subscriptions', views.SubscribersView)


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register-user'), 
    path('login/', views.LoginApiView.as_view(), name='login-user'),
    path('post-like/', views.LikePostView.as_view(), name='like-post'), 
    path('post-saves/', views.SavedPostView.as_view(), name='saved-post'), 
    path('post-subscribe/<int:user_id>/', views.SubscribeView.as_view(), name='subscribe-user'),  
    path('user-subscriptions/', views.MySubscriptionsView.as_view(), name='user-subscriptions'), 
    path('', include(router.urls)),  
]

urlpatterns += url_doc

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
