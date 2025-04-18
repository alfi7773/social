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
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None)
        return Post.objects.create(user=user, **validated_data)



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['subscriber', 'author', 'created_at']


class UserWithAreaSerializer(serializers.Serializer):
    user_posts = PostSerializer(source='post', many=True, read_only=True)
    favorite_posts = serializers.SerializerMethodField()
    saved_posts = serializers.SerializerMethodField()
    subscribes = serializers.SerializerMethodField()
    subscribers = serializers.SerializerMethodField()
    
    def get_saved_posts(self, obj):
        saved = obj.saved.first()
        if not saved:
            return []
        posts = [item.post for item in saved.saved_items.all()]
        return PostSerializer(posts, many=True).data

    def get_subscribes(self, obj):
        return list(obj.subscriptions.values_list('author__id', flat=True))

    def get_subscribers(self, obj):
        return list(obj.subscribers.values_list('subscriber__id', flat=True))

    def get_favorite_posts(self, obj):
        likes = Like.objects.filter(user=obj)
        post_ids = LikeItem.objects.filter(like__in=likes).values_list('post', flat=True)
        posts = Post.objects.filter(id__in=post_ids)
        return PostSerializer(posts, many=True).data

    def get_subscribers_count(self, obj):
        return obj.subscribers.count()

    def get_subscribes_count(self, obj):
        return obj.subscriptions.count()

class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['id','avatar', 'username', 'email', 'first_name', 'last_name']


    def get_mass(self, obj):
        return UserWithAreaSerializer(obj).data
    
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class RegisterSerializer(serializers.ModelSerializer):
    
    avatar = serializers.ImageField(required=False, allow_null=True)
    mass = serializers.SerializerMethodField()


    class Meta:
        model = MyUser   
        fields = '__all__'
        fields = ['id','avatar','username', 'email', 'first_name', 'last_name', 'password', 'mass'] 


    def get_mass(self, obj):
        return UserWithAreaSerializer(obj).data

    

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
        user = validated_data['user']

        saved_instance, created = Saved.objects.get_or_create(user=user)

        for item_data in saved_items_data:
            SavedItem.objects.create(saved=saved_instance, **item_data)

        return saved_instance

    
class PostOnlySerializer(serializers.Serializer):
    post = serializers.IntegerField()

class UserLikesSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    saved_items = PostOnlySerializer(many=True)



    
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
        return UserWithAreaSerializer(obj).data