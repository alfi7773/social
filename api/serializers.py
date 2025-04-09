from social.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from social.models import *
from django.contrib.auth import get_user_model

User = get_user_model()






class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'username', 'first_name', 'last_name', 'avatar']



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    # username = serializers.CharField(required=False)  

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'username', 'first_name', 'last_name', 'avatar']  

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            avatar=validated_data['avatar'],
            useranme=validated_data['useranme'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )


        return user
    
class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    


class ImageUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUserImage
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
    
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Like
        fields = ['user', 'post']
        
        
    def get_user(self, obj):
        return obj.user.id
        
class SavedItemSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = SavedItem
        fields = ['post']



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
    
    # comment = CommentSerializer(many=True)
    likes = serializers.IntegerField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        exclude = ('saved',)
        
    def get_avatar(self, obj):
        return obj.user.avatar.url if obj.user.avatar else None
        
        
class MyUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = '__all__'