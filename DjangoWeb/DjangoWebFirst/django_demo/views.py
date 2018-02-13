from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django_demo.models import People
from django.template import Context, Template


# Create your views here.
def first_try(request):
    person = People(name='jack', job='officer')
    html_string = '''
        <html>
            <head>
                <meta charset="utf-8">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.6/semantic.css" media="screen" title="no title">
                <title>diango</title>
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
