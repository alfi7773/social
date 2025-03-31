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
router.register('saved', views.SavedViewSet)
router.register('tags', views.TagViewSet)
router.register('image-user', views.UserImage)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('likes/', views.LikePostView.as_view(), name='like_post'),
    path('', include(router.urls)),  
]

urlpatterns += url_doc
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
