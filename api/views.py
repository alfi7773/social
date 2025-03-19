from django.shortcuts import render

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

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class SavedViewSet(viewsets.ModelViewSet):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer