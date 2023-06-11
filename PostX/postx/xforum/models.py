from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your models here.
class Xforum(models.Model):
    title=models.CharField(max_length=255, verbose_name="Title")
    user_name = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, verbose_name="Username")
    time_to_read=models.IntegerField(verbose_name="Time to read")
    photo=models.ImageField(upload_to="photos/%Y/%m/%d/",blank=True, verbose_name="Image")
    content=models.TextField(blank=True, verbose_name="Body")
    slug = models.SlugField(max_length=50, db_index=True, unique=True, verbose_name="Url")
    time_create=models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update=models.DateTimeField(auto_now=True, verbose_name="Time update")
    is_published=models.BooleanField(default=True, verbose_name="Is published")
    cat=models.ForeignKey('Category', on_delete=models.CASCADE, null=True, verbose_name="Category")
    likes=models.ManyToManyField(get_user_model(), blank=True, related_name='blog_posts')


    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug":self.slug,})

    def __str__(self):
        return self.title


    class Meta:
        verbose_name="Статьи"
        verbose_name_plural="Статьи"
        ordering = ['-time_create']

class Category(models.Model):
    name=models.CharField(max_length=100, db_index=True)
    slug=models.SlugField(max_length=50, db_index=True, unique=True, verbose_name="Url")


    def get_absolute_url(self):

        return reverse('category', kwargs={"cat_slug":self.slug,})


    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = "Категории"
        verbose_name_plural = "Категории"



class Comments(models.Model):
    article = models.ForeignKey(Xforum, related_name='comments', on_delete=models.CASCADE)
    comment_author=models.ForeignKey(User, related_name='user_comment', on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)




    def __str__(self):
        return '%s - %s' % (self.article.title, self.comment_author)

    def total_comments(self):
        return self.body.count()

class Profile(models.Model):
    user=models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, null=True)
    bio=models.TextField()
    profile_pic=models.ImageField(upload_to='photos/profile_images/%Y/%m/%d/', null=True, blank=True)
    web_site_url=models.CharField(max_length=255, blank=True, null=True)
    twitter_url=models.CharField(max_length=255, blank=True, null=True)
    instagram_url=models.CharField(max_length=255, blank=True, null=True)
    vk_url=models.CharField(max_length=255, blank=True, null=True)
    linkdn_url=models.CharField(max_length=255, blank=True, null=True)






    def __str__(self):
        return str(self.user)