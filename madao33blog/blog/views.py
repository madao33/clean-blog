from django.shortcuts import get_object_or_404, render
from .models import Article, Category
import markdown

def index(request):
    latest_article_list = Article.objects.order_by('-modified_time')
    context = {'latest_article_list': latest_article_list}
    return render(request, 'index.html', {'author': "madao33", "article_list": latest_article_list})

def about(request):
    return render(request, 'about.html')

def post(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.increase_views()
    md = markdown.Markdown(extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                    ])
    article.body = md.convert(article.body)
    return render(request, 'post.html', {"article": article, 'toc': md.toc})

def category(request):
    category_list = Category.objects.order_by('-createdTime')
        
    return render(request, 'category.html', {"author": "madao33", "category_list":category_list})


def category_detail(request, cat):
    articles = Article.objects.filter(category__category=cat)
    catgory = get_object_or_404(Category, category=cat)

    return render(request, 'category_detail.html', {'author':"madao33", "article_list":articles, "category": catgory})


def tag(request, tag):
    articles = Article.objects.filter(tags__name=tag)
    
    return render(request, 'about.html', {"article": articles, "tag": tag})