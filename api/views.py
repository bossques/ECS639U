from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.conf import settings

from . import models


class MissingFieldsError(Exception):
    def __init__(self, fields: list[str]):
        self.fields = fields
        super().__init__('Missing fields: ' + ', '.join(fields))


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


def get_form(request: HttpRequest, *fields):
    form = {}
    for field in fields:
        form[field] = request.POST.get(field, None)

    empty_fields = [field_name for field_name, value in form.items() if value is None]
    if empty_fields:
        raise MissingFieldsError(fields=empty_fields)

    return form


def serialize_user(request: HttpRequest, user: models.User) -> dict:
    profile_url = request.build_absolute_uri(
        settings.MEDIA_URL + str(user.profile_image)
    ) if user.profile_image else None

    return {
        'id': user.id,
        'email': user.email,
        'date_of_birth': user.date_of_birth,
        'profile_url': profile_url
    }


@csrf_exempt
@require_http_methods('POST')
def login_view(request: HttpRequest) -> HttpResponse:
    try:
        form = get_form(request, 'email', 'password')
    except MissingFieldsError as e:
        return JsonResponse({field: 'missing' for field in e.fields}, status=404)

    user = authenticate(
        request,
        username=form['email'],
        password=form['password']
    )

    if user is not None:
        login(request, user)
        json = serialize_user(request, user)
        return JsonResponse(json, status=200)
    else:
        json = {'message': 'Incorrect username or password.'}
        return JsonResponse(json, status=400)


@csrf_exempt
@require_http_methods('POST')
def register_view(request: HttpRequest) -> HttpResponse:
    try:
        form = get_form(request, 'email', 'password', 'date_of_birth')
    except MissingFieldsError as e:
        return JsonResponse({field: 'missing' for field in e.fields}, status=404)

    try:
        user = models.User.objects.create_user(
            username=form['email'],
            email=form['email'],
            password=form['password'],
            date_of_birth=form['date_of_birth']
        )
    except IntegrityError:
        return HttpResponse(status=409)

    json = serialize_user(request, user)
    return JsonResponse(json, status=200)
