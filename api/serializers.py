from social.models import *
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Tag
        fields = '__all__'
        

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'
        
class LikeSerializer(serializers.ModelSerializer):
    
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    
    class Meta:
        model = Like
        exclude = ['user',]
        

class SavedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Saved
        fields = '__all__'
        
        
class PostSerializer(serializers.ModelSerializer):
    
    tags = TagSerializer(many=True)
    # comment = CommentSerializer(many=True)
    likes = LikeSerializer()
    # saved = SavedSerializer()
    
    class Meta:
        model = Post
        fields = '__all__'