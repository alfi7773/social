from django.contrib import admin
from social.models import *

admin.site.register(MyUser)
admin.site.register(Post)
admin.site.register(MyUserImage)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Saved)
admin.site.register(Tag)

# Register your models here.
