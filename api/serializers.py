from social.models import *
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Tag
        fields = '__all__'

        
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        replies = obj.replies.filter()
        return CommentSerializer(replies, many=True).data

        
class LikeSerializer(serializers.ModelSerializer):
    
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    
    
    class Meta:
        model = Like
        exclude = ['user',]
        
        
class SavedItemSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = SavedItem
        fields = ['post', 'quantity']


class SavedSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    saved_items = SavedItemSerializer(many=True)

    class Meta:
        model = Saved
        fields = ['user', 'saved_items']

    def create(self, validated_data):
        saved_items_data = validated_data.pop('saved_items')
        saved_instance = Saved.objects.create(**validated_data)
        for item_data in saved_items_data:
            SavedItem.objects.create(saved=saved_instance, **item_data)
        return saved_instance
        
class PostSerializer(serializers.ModelSerializer):
    
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    # comment = CommentSerializer(many=True)
    likes = LikeSerializer(many=False, read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    saved_items = SavedItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'