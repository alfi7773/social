from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_resized import ResizedImageField

class TimeAbstract(models.Model):
    
    created_at = models.DateField('created', auto_now_add=True)
    updated_at = models.DateField('', auto_now=True)
    
    class Meta:
        abstract = True
        

class MyUser(TimeAbstract):
    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    change_percentage = models.FloatField(verbose_name="Изменение",default=0)


    def __str__(self):
        return self.user.username
    
    
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


class Comment(TimeAbstract):
    post = models.ForeignKey('social.Post', related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]


class Like(TimeAbstract):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ManyToManyField('social.Post', through='LikeItem')
    
class LikeItem(TimeAbstract):
    like = models.ForeignKey('social.Like', related_name='like_items', on_delete=models.PROTECT)
    post = models.ForeignKey('social.Post', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)



class Saved(TimeAbstract):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ManyToManyField('social.Post', through='SavedItem')
    
class SavedItem(TimeAbstract):
    saved = models.ForeignKey('social.Saved', related_name='saved_items', on_delete=models.PROTECT)
    post = models.ForeignKey('social.Post', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)





class Post(TimeAbstract):
    
    class Meta:
        verbose_name_plural = 'посты'
        verbose_name = 'пост'
        
    image = ResizedImageField(upload_to='posts/', quality=90, force_format='WEBP', null=True, blank=True)
    description = models.TextField(verbose_name='описание поста')
    tags = models.ManyToManyField('social.Tag', related_name='post')
    user = models.ForeignKey('social.MyUser', on_delete=models.PROTECT,related_name='post')
    likes = models.PositiveIntegerField(verbose_name='лайки', default=0)
    
    def __str__(self):
        return self.description
       

# Create your models here.
