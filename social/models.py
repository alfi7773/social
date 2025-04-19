from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField
from .manages import MyUserManager
from django.conf import settings


class TimeAbstract(models.Model):
    
    created_at = models.DateField('created', auto_now_add=True)
    updated_at = models.DateField('', auto_now=True)
    
    class Meta:
        abstract = True
        

class MyUser(AbstractBaseUser, PermissionsMixin, TimeAbstract):
    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    avatar = ResizedImageField('аватарка', size=[500, 500], crop=['middle', 'center'],
                               upload_to='avatars/', force_format='WEBP', quality=90,
                               null=True, blank=True)
    username = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField('электронная почта', unique=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    change_percentage = models.FloatField(verbose_name="Изменение", default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = ['username',]  

    def __str__(self):
        return self.email

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
    
    def get_avatar(self):
        if hasattr(self, 'artist_image') and self.artist_image.image:
            return self.artist_image.image.url
        return None


    @property
    def subscribers_count(self):
        return self.subscribers.count()

    @property
    def subscriptions_count(self):
        return self.subscriptions.count()

    
class MyUserImage(TimeAbstract):
    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"

    artist = models.OneToOneField(
        'social.MyUser',
        on_delete=models.CASCADE,
        related_name="artist_image",
        verbose_name="Фото пользователя",
    )
    image = models.ImageField(upload_to="artist_images/", verbose_name="Фото")

    def __str__(self):
        return f"Image of {self.artist.username}"
    
    


class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Comment(TimeAbstract):
    post = models.ForeignKey('social.Post', related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]


class Like(TimeAbstract):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    post = models.ManyToManyField('social.Post', through='LikeItem')
    
class LikeItem(TimeAbstract):
    like = models.ForeignKey('social.Like', related_name='like_items', on_delete=models.PROTECT)
    post = models.ForeignKey('social.Post', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)



class Saved(TimeAbstract):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='saved')
    post = models.ManyToManyField('social.Post', through='SavedItem', related_name='saved_posts')
    
class SavedItem(TimeAbstract):
    saved = models.ForeignKey('social.Saved', related_name='saved_items', on_delete=models.PROTECT)
    post = models.ForeignKey('social.Post', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)





class Post(TimeAbstract):
    
    class Meta:
        verbose_name_plural = 'посты'
        verbose_name = 'пост'
        
    # file = models.FileField(upload_to='posts/', blank=True, null=True)
    title = models.CharField(verbose_name='заголоыок поста', max_length=200, blank=True, null=True)
    description = models.TextField(verbose_name='описание поста', blank=True, null=True)
    user = models.ForeignKey('social.MyUser', on_delete=models.PROTECT,related_name='post')
    likes = models.PositiveIntegerField(verbose_name='лайки', default=0, blank=True, null=True)
    saved = models.PositiveIntegerField(verbose_name='сохраненные', default=0, blank=True, null=True)
    
    def __str__(self):
        return self.title
       
       
    @property
    def image(self):
        if self.images.first():
            return self.images.first().image
        return None
       
class PostImage(TimeAbstract):
    class Meta:
        verbose_name = 'изображение поста'
        verbose_name_plural = 'изображении постов'
        # ordering = ('-created_at',)

    post = models.ForeignKey('social.Post', models.CASCADE, related_name='images', verbose_name='image')
    media = ResizedImageField('изображение', upload_to='post_images/', quality=90, force_format='WEBP')

    def __str__(self):
        return f'{self.post.title}'
       
       
class Subscription(models.Model):
    subscriber = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='subscriptions')
    author = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'author')  



class PostTag(TimeAbstract):
    class Meta:
        verbose_name = 'tag post'
        verbose_name_plural = 'tags posts'
        # ordering = ('-created_at',)

    name = models.CharField('название', max_length=50)
    post = models.ForeignKey('social.Post', models.CASCADE, related_name='post_tags', verbose_name='tag')

    def __str__(self):
        return f'{self.name}'

# Create your models here.
 