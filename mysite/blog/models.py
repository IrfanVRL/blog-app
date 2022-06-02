from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


def user_directory_path(instance,filename):
      return 'posts/{0}/{1}'.format(instance.id,filename)
class Category(models.Model):
      name = models.CharField(max_length=100)
      def __str__(self):
            return self.name
class Post (models.Model):
      class NewManager(models.Manager):
            def get_queryset(self):
                  return super().get_queryset() .filter(status='published')
      options = (
      ('draft', 'Draft'),
      ('published', 'Published'),
      )
      #admin sayfasındaki özellikler bunlar

      title  = models.CharField(max_length=250) # title of every posts
      category = models.ForeignKey(Category,on_delete = models.PROTECT, default = 1)
      excerpt = models.TextField(null = True)   # excerpts
      image = models.ImageField(upload_to=user_directory_path, default='posts/default.jpg ') #identify image model
      slug = models.SlugField(max_length=250,unique_for_date= 'publish')
      publish = models.DateTimeField(default=timezone.now)  # draft and publish model to manage posts visibility
      author = models.ForeignKey(User, on_delete=models.CASCADE,related_name= 'blog_posts')
      content = models.TextField()
      status = models.CharField(max_length=10,choices=options,default='draft') # statu özellikleri yukarda belirtildi
      objects = models.Manager()
      newmanager = NewManager()

      def get_absolute_url(self):
            return reverse('blog:post_single',args = [self.slug])
      class Meta:
            ordering = ('-publish',)
      def __str__(self):
            return self.title

class Comment(models.Model):
      post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name= 'comments')
      name = models.CharField(max_length=50)
      email = models.EmailField()
      content = models.TextField()
      publish = models.DateTimeField(auto_now_add=True)
      status = models.BooleanField(default=True)

   