from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from .yasg import urlpatterns as url_doc
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)
# router.register('likes', views.LikePostView)
router.register('saved', views.SavedViewSet, basename='save')
router.register('post-save', views.SavedPostViewSet)
router.register('tags', views.PostTagViewSet)
router.register('image-user', views.UserImage)

router.register('users', views.AllUser)
router.register('like', views.PostsByUserView, basename='user-likes')
router.register('subscribers', views.SubscribersView)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('likes/', views.LikePostView.as_view(), name='like_post'),
    path('subscribe/<int:user_id>/', views.SubscribeView.as_view()),
    path('subscriptions/', views.MySubscriptionsView.as_view(), name='subscriptions'),
    # path('users/', views.AllUser.as_view()),
    path('', include(router.urls)),  
]

urlpatterns += url_doc
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)