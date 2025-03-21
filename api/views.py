from django.shortcuts import render
from django.db.models import F
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api import models
from social.models import Post, LikeItem
from django.contrib.auth.models import User

# Create your views here.
from rest_framework import viewsets
from social.models import Post, Comment, Like, Saved, Tag
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, SavedSerializer, TagSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


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

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer