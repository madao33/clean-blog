from datetime import datetime, timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.db.models.fields import CharField, NullBooleanField
from django.shortcuts import get_object_or_404
from mdeditor.fields import MDTextField

class User(models.Model):
    """
    用户注册模型
    """

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    createdTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        """
        检查用户账号和密码是否符合规范
        """
        if len(self.name) >= 100:
            raise ValidationError({"User": "Username is too long!"})
        elif len(self.password) >= 100:
            raise ValidationError({"User": "User passwrod is too long"})

class Category(models.Model):
    """
    文章分类模型
    """

    category = models.CharField(max_length=128, unique=True)
    describtion = models.CharField(max_length=1024)
    createdTime = models.DateTimeField(auto_now_add=True)
    articles = models.PositiveBigIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='作者')
    
    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
    

class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name
    
    

class Article(models.Model):
    title = models.CharField(max_length=128, default='主标题', unique=True, verbose_name='主标题')
    subtitle = models.CharField(max_length=128, default='副标题', verbose_name='副标题')
    # body = models.TextField(verbose_name="文章内容")
    body = MDTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, verbose_name='分类')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='作者')
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    modified_time = models.DateTimeField("修改时间")
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    views = models.PositiveBigIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time', 'title']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwrags):
        self.modified_time = datetime.now()
        category = get_object_or_404(Category, category=self.category.category)
        articles = Article.objects.filter(category__category=self.category.category)
        count = 0
        for article in articles:
            count += 1
        category.articles = count
        category.save()
        super().save(*args, **kwrags)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    
