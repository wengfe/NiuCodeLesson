from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django_demo.models import People, Article, Comment
from django.template import Context, Template
from django_demo.form import CommentForm


# Create your views here.
def first_try(request):
    person = People(name='jack', job='officer')
    html_string = '''
        <html>
            <head>
                <meta charset="utf-8">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.6/semantic.css" media="screen" title="no title">
                <title> django </title>
            </head>
            <body>
                <h1 class="ui center aligned icon header">
                    <i class="hand spock icon"></i>
                    Hello, {{ person.name }}
                </h1>
            </body>
        </html>
    '''
    # 将 html 字符转成模板
    t = Template(html_string)
    # 组上下文
    c = Context({'person': person})
    # 渲染模板
    web_page = t.render(c)
    return HttpResponse(web_page)


def index(request):
    print(request)
    print('===' * 30)
    print(dir(request))
    print('===' * 30)
    print(type(request))

    queruseet = request.GET.get('tag')
    print(queruseet)

    if queruseet:
        article_list = Article.objects.filter(tag=queruseet)
    else:
        # 数据库操作方法，从指定表中取得所有值  table_mame.objects.all()
        article_list = Article.objects.all()

    context = {}

    # 往字典中填入数据
    context['article_list'] = article_list
    index_page = render(request, 'first_web_2.html', context)
    return index_page


def detail(request):
    if request.method == 'GET':
        form = CommentForm
    if request.method == 'POST':
        # 绑定表单， 是进行数据校验的前置步骤
        form = CommentForm(request.POST)
        # 判断绑定的表单是否通过数据验证
        if form.is_valid():
            # 表单数据通过后，会将数据存储在 cleaned_data 中
            name = form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            c = Comment(name=name, comment=comment)
            c.save()
            # redirect 重定向回 name=detail 的 url
            return redirect(to='detail')
    context = {}
    comment_list = Comment.objects.all()
    context['comment_list'] = comment_list
    context['form'] = form
    return render(request, 'detail.html', context)
