from django.shortcuts import get_object_or_404, render
from django.db.models import F
from rest_framework import status
from rest_framework.views import APIView
from api import models
from social.models import Like, MyUser, MyUserImage, Post, LikeItem, PostTag, Subscription
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from collections import defaultdict


# Create your views here.
from rest_framework import viewsets
from social.models import Post, Comment, Saved
from .serializers import LikeSerializer, MyUserIdSerializer, MyUserSerializer, PostSerializer, CommentSerializer, PostTagSerializer, RegisterSerializer, SavedSerializer, SubscriptionSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, ReadUserSerializer, ImageUserSerializer, UserLikesSerializer


class AllUser(viewsets.ModelViewSet):
    
    queryset = MyUser.objects.all()
    serializer_class = MyUserIdSerializer

class LoginApiView(APIView):
    

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email, password = serializer.validated_data.get('email'), serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            read_serializer = MyUserIdSerializer(user, context={'request': request})

            data = {
                **read_serializer.data,
                'token': token.key,
                'user': read_serializer.data
            }

            return Response(data)

        return Response({'detail': 'Пользователь не найден или не правильный пароль.'}, status=status.HTTP_400_BAD_REQUEST)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("Authentication credentials were not provided.")
        

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def posts_by_user(self, request, user_id=None):
        posts = self.queryset.filter(user__id=user_id)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserImage(viewsets.ModelViewSet):
    queryset = MyUserImage.objects.all()
    serializer_class = ImageUserSerializer


class LikePostView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get('post')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        like, like_created = Like.objects.get_or_create(user=user)
        like_item, item_created = LikeItem.objects.get_or_create(like=like, post=post)

        if not item_created:
            return Response({"status": "already liked"})

        post.likes += 1
        post.save()
        

        return Response({"status": "liked"})


class PostsByUserView(viewsets.ModelViewSet):
    
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def posts_by_user(self, request, user_id=None):
        like_items = LikeItem.objects.filter(like__user__id=user_id)

        data = defaultdict(list)
        for item in like_items:
            post_data = PostSerializer(item.post).data
            user_id = item.like.user.id
            data[user_id].append(PostSerializer(item.post).data)


        result = [{'user': uid, 'like_items': items} for uid, items in data.items()]
        serializer = UserLikesSerializer(result, many=True)
        return Response(serializer.data)

        posts = self.queryset.filter(user__id=user_id)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


    

class SubscribersPostView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user')
        post_id = request.data.get('post')
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        post.likes += 1
        post.save()
        return Response({"status": "liked"})
    
class SavedPostViewSet(viewsets.ModelViewSet):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer



class SavedViewSet(viewsets.ModelViewSet):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def saved_by_user(self, request, user_id=None):
        saved_instances = self.queryset.filter(user__id=user_id)
        serializer = self.get_serializer(saved_instances, many=True)
        return Response(serializer.data) 
        
    def posts_by_user(self, request, user_id=None):
        posts = self.queryset.filter(user__id=user_id)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response (
            {"message": "Пользователь создан",  
            "user": user,
            },
            status=status.HTTP_201_CREATED
        )
        
        
class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        author = get_object_or_404(MyUser, id=user_id)
        if request.user == author:
            return Response({"detail": "Нельзя подписаться на себя."}, status=400)

        subscription, created = Subscription.objects.get_or_create(
            subscriber=request.user,
            author=author
        )
        if not created:
            return Response({"detail": "Уже подписан."}, status=400)
        return Response({"detail": "Подписка оформлена."}, status=201)

    def delete(self, request, user_id):
        author = get_object_or_404(MyUser, id=user_id)
        subscription = Subscription.objects.filter(subscriber=request.user, author=author)
        if subscription.exists():
            subscription.delete()
            return Response({"detail": "Подписка удалена."}, status=204)
        return Response({"detail": "Вы не были подписаны."}, status=400)

class SubscribersView(viewsets.ModelViewSet):
    
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def subscribers_by_user(self, request, user_id=None):
        subscriptions = self.queryset.filter(author__id=user_id)
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)
    


class MySubscriptionsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyUserIdSerializer  

    def get_queryset(self):
        return MyUser.objects.filter(subscribers__subscriber=self.request.user)
    
    
class PostTagViewSet(viewsets.ModelViewSet):
    
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer