from social.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from social.models import *
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied


User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        replies = obj.replies.all() 
        return CommentSerializer(replies, many=True).data

class UsernameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = ['username', 'id']


        
class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)

    # user = UsernameSerializer()
    avatar = serializers.SerializerMethodField(read_only=True)
    user = UsernameSerializer(read_only=True)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        exclude = ('saved', )
        
    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.user.avatar and request:
            return request.build_absolute_uri(obj.user.avatar.url)
        return None

class UserWithAreaSerializer(serializers.Serializer):


    user_posts = PostSerializer(many=True)
    favorite_posts = serializers.CharField()
    saved_posts = serializers.CharField()
    subscribes = serializers.CharField()
    subscribers = serializers.CharField()

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
    




class ReadUserSerializer(serializers.ModelSerializer):

    mass = serializers.SerializerMethodField()


    class Meta:
        model = MyUser
        fields = ['id','avatar', 'username', 'email', 'first_name', 'last_name', 'mass']


    def get_mass(self, obj):
        return UserWithAreaSerializer({
            "user_posts": [],
            "favorite_posts": [],
            "saved_posts": [],
            "subscribes": [],
            "subscribers": [],
        }).data 
        



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class RegisterSerializer(serializers.ModelSerializer):
    
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = MyUser
        fields = '__all__'
        # fields = ['id','avatar','username', 'email', 'first_name', 'last_name', 'password'] 

    def create(self, validated_data):
        user = MyUser.objects.create_user (
            avatar=validated_data['avatar'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        # print(user)
        return ReadUserSerializer(user).data
    
class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    



class ImageUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUserImage
        fields = '__all__'



        


        
class LikeSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Like
        fields = ['user', 'post']
        
        
    def get_user(self, obj):
        return obj.user.id
        






    
class MyUserSerializer(serializers.ModelSerializer):

    mass = serializers.SerializerMethodField()
    
    class Meta:
        model = MyUser
        fields = ['avatar','username', 'email', 'first_name', 'last_name', 'password', 'mass']


class MyUserIdSerializer(serializers.ModelSerializer):

    mass = serializers.SerializerMethodField()
    
    class Meta:
        model = MyUser
        fields = ['id','avatar','username', 'email', 'first_name', 'last_name', 'password', 'mass']


    def get_mass(self, obj):
        return UserWithAreaSerializer({
            "user_posts": [],
            "favorite_posts": [],
            "saved_posts": [],
            "subscribes": [],
            "subscribers": [],
        }).data 
        


