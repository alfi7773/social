from social.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from social.models import *
from django.contrib.auth import get_user_model

User = get_user_model()



class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()


class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        )



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
        fields = ['email', 'password', 'username']  

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
        )

        my_user = MyUser.objects.create(user=user, email=validated_data['email'])
        return my_user
    # def create(self, validated_data):
    #     user = MyUser.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data.get('email', ''),
    #         password=validated_data['password']
    #     )
    


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
    
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    # comment = CommentSerializer(many=True)
    likes = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    saved_items = SavedItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'