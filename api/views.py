import json

from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.conf import settings

from .forms import LoginForm, RegisterForm, ModifyForm
from .models import Article, ArticleCategory, ArticleComment, User


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


@require_http_methods(['POST', 'GET'])
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return redirect(to='home')
    else:
        form = LoginForm()

    return render(request, 'api/auth/login.html', {'form': form})


@require_http_methods(['POST', 'GET'])
def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(to='home')
    else:
        form = RegisterForm()

    return render(request, 'api/auth/register.html', {'form': form})


@require_http_methods(['POST'])
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponse(status=200)


@require_http_methods(['GET', 'POST'])
def profile_view(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if request.method == 'GET':
        return JsonResponse(status=200, data=serialize_user(request.user, request))
    else:
        form = ModifyForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse(status=200, data=serialize_user(request.user, request))
        else:
            return JsonResponse(status=400, data=form.errors.as_json(), safe=False)


@require_http_methods(['PUT'])
def category_view(request: HttpRequest, category_id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    category = get_object_or_404(ArticleCategory, id=category_id)

    favourite_categories = request.user.favourite_categories
    if category in favourite_categories.all():
        favourite_categories.remove(category)
    else:
        favourite_categories.add(category)

    return JsonResponse(status=200, data=serialize_user(request.user, request))


@require_http_methods(['GET'])
def articles_view(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.order_by('created_at')
    articles = [article.to_dict() for article in articles]

    categories = ArticleCategory.objects.all()
    categories = [category.to_dict() for category in categories]

    response = {
        'categories': categories,
        'articles': articles
    }

    return JsonResponse(status=200, data=response, safe=False)


@require_http_methods(['GET'])
def article_view(request: HttpRequest, article_id: int) -> HttpResponse:
    article = get_object_or_404(Article, id=article_id)
    comments = ArticleComment.objects.filter(article=article).order_by('-created_at')

    response = article.to_dict()
    response['comments'] = [serialize_comment(comment, request) for comment in comments]

    return JsonResponse(status=200, data=response, safe=False)


@require_http_methods(['POST'])
def comments_view(request: HttpRequest, article_id: int):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    article = get_object_or_404(Article, id=article_id)

    response = json.loads(request.body)
    reply_to = response.get('reply_to', None)
    if reply_to is not None:
        reply_to = get_object_or_404(ArticleComment, id=reply_to, article=article)

    comment = response.get('comment', None)
    if comment is None:
        return HttpResponse(status=403)

    article_comment = ArticleComment(
        article=article,
        belongs_to=request.user,
        comment=comment,
        reply_to=reply_to
    )
    article_comment.save()

    return JsonResponse(status=200, data=serialize_comment(article_comment, request), safe=False)


@require_http_methods(['PUT', 'DELETE'])
def comment_view(request: HttpRequest, article_id: int, comment_id: int):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    article = get_object_or_404(Article, id=article_id)
    article_comment = get_object_or_404(ArticleComment, id=comment_id, article=article)

    if request.method == 'PUT':
        response = json.loads(request.body)
        comment = response.get('comment', None)
        if comment is None:
            return HttpResponse(status=403)

        article_comment.comment = comment
        article_comment.save()
        return HttpResponse(status=200)
    elif request.method == 'DELETE':
        article_comment.delete()
        return HttpResponse(status=200)


def serialize_user(user: User, request: HttpRequest):
    profile_url = request.build_absolute_uri(
        settings.MEDIA_URL + str(user.profile_image)
    ) if user.profile_image else None

    if request.is_secure() and profile_url and profile_url.startswith('http://'):
        profile_url = profile_url.replace('http://', 'https://')

    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'profile_url': profile_url,
        'date_of_birth': user.date_of_birth,
        'favourite_categories': list(user.favourite_categories.values('id', 'name'))
    }


def serialize_comment(comment: ArticleComment, request: HttpRequest):
    return {
        'id': comment.id,
        'article': comment.article.to_dict(),
        'belongs_to': serialize_user(comment.belongs_to, request),
        'comment': comment.comment,
        'reply_to': comment.reply_to.to_dict() if comment.reply_to else None,
        'created_at': comment.created_at
    }
