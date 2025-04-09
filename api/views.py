from django.shortcuts import render
from django.db.models import F
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api import models
from social.models import MyUser, MyUserImage, Post, LikeItem
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny


# Create your views here.
from rest_framework import viewsets
from social.models import Post, Comment, Saved
from .serializers import MyUserSerializer, PostSerializer, CommentSerializer, RegisterSerializer, SavedSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, ReadUserSerializer, ImageUserSerializer


class AllUser(viewsets.ModelViewSet):
    
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

class LoginApiView(APIView):
    

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email, password = serializer.validated_data.get('email'), serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            read_serializer = ReadUserSerializer(user, context={'request': request})

            data = {
                **read_serializer.data,
                'token': token.key
            }

            return Response(data)

        return Response({'detail': 'Пользователь не найден или не правильный пароль.'}, read_serializer.data, status=status.HTTP_400_BAD_REQUEST)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserImage(viewsets.ModelViewSet):
    queryset = MyUserImage.objects.all()
    serializer_class = ImageUserSerializer


class LikePostView(APIView):
    
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


class SavedViewSet(viewsets.ModelViewSet):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer


    
class RegisterView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # token, created = Token.objects.get_or_create(user=user)
        print(user)
        return Response (
            {"message": "Пользователь создан",  
            # "token": token.key,
            "user": user,
            },
            status=status.HTTP_201_CREATED
        )