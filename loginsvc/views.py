import hashlib
import logging
import random
import string

from django.conf import settings
from django.http import JsonResponse
from django.http.request import QueryDict
from django.utils import timezone
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import AccessToken, Application, RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_condition import Or

from account.models import Staff
from loginsvc.permissions import IsStaff, IsManager, IsSeller
from loginsvc.forms import LoginForm, RetSetPassword
from demo.lib import constans
from demo.utils import get_user_type


logger = logging.getLogger(__name__)


def random_token_generator(length):
    seq = string.ascii_lowercase + string.digits

    return ''.join(random.choices(seq, k=length))


def generate_token(string_0, string_1):

    salt = random_token_generator(4)
    token = f'{string_0}.{string_1}.{salt}'

    return hashlib.md5(token.encode('utf-8')).hexdigest()


def generate_response(code, msg=None, data=None):
    response = {'code': code,
                'msg': msg,
                'data': data}

    return JsonResponse(response, status=200)


def compose_error_response(message, status_code=constans.NOT_OK):
    return JsonResponse(
        {'msg': message,
         'code': status_code,
         'data': None})


def __check_dashboard_login(request, user_obj):
    if request.path == '/v1/manage/login/':
        staff = user_obj.staff_user
        if staff and (staff.is_manager or staff.is_staff):
            return 'dashboard'
        else:
            return False
    else:  # normal login always True
        return 'fronted'


def delete_token(user, application=None):
    dic = {'user': user}
    if application:
        dic['application'] = application
    AccessToken.objects.filter(**dic).delete()
    RefreshToken.objects.filter(**dic).delete()


def create_token(user, app, delete_all=True):
    expire_seconds = settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']
    scopes = ' '.join(settings.OAUTH2_PROVIDER['SCOPES'].keys())

    # delete old tokens, if any
    if delete_all:
        delete_token(user, app)

    expires = timezone.localtime() + timezone.timedelta(seconds=expire_seconds)

    access_token = AccessToken.objects.create(
        user=user,
        application=app,
        token=generate_token(user.username,
                             expires.strftime('%Y-%m-%d %H:%M:%S')),
        expires=expires,
        scope=scopes)

    refresh_token = RefreshToken.objects.create(
        user=user,
        application=app,
        token=generate_token(user.username,
                             expires.strftime('%Y-%m-%d %H:%M:%S')),
        access_token=access_token)

    token = {
        'access_token': access_token.token,
        'token_type': 'Bearer',
        'expires_in': expires,
        'refresh_token': refresh_token.token,
        'scope': access_token.scope
    }
    return token


@api_view(['POST'])
@csrf_exempt
@permission_classes([])
def login(request):
    data = request.POST or QueryDict(request.body)  # to capture data in IE
    form = LoginForm(data)
    if not form.is_valid():
        return compose_error_response('无效的用户名或密码')
    user = User.objects.filter(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return compose_error_response('无效的用户名或密码')

    if not user.staff_user.status == Staff.STAFF_ACTIVE:
        return compose_error_response('此帐户已被暂停使用')

    application = __check_dashboard_login(request, user)
    if not application:
        return compose_error_response('此帐户无法登录管理中心')
    app = Application.objects.get(name=application)
    data_d = create_token(user, app, False)
    response = JsonResponse(data_d, status=200)
    response.set_cookie(key='access_token',
                        value=data_d['access_token'])
    response.set_cookie(key='refresh_token',
                        value=data_d['refresh_token'])
    response.set_cookie(key='auth_req', value='')

    return response


@csrf_exempt
@api_view(['POST'])
@permission_classes([Or(IsSeller, IsManager, IsStaff)])
def logout(request):
    token = request.auth
    token_obj = AccessToken.objects.filter(token=token).first()
    token_obj.delete()
    return generate_response(constans.ALL_OK)


@csrf_exempt
@permission_classes([Or(IsSeller, IsManager, IsStaff)])
@api_view(['GET'])
def current_user(request):
    user = request.user
    if not user:
        return JsonResponse(data=constans.NOT_OK,
                            status=404)
    return generate_response(data={'username': user.username,
                                   'role': get_user_type(user)},
                             code=constans.ALL_OK, msg=None)


@csrf_exempt
@permission_classes([Or(IsSeller, IsManager, IsStaff)])
@api_view(['POST'])
def reset_password(request):
    data = request.POST or QueryDict(request.body)  # to capture data in IE
    form = RetSetPassword(data)
    if not form.is_valid():
        return compose_error_response('请求数据错误, 请输入5-16位的新密码')

    if not request.user.check_password(data['old_password']):
        return compose_error_response('旧密码错误')

    if data['new_password'] != data['con_password']:
        return compose_error_response('两次密码不相等')
    with transaction.atomic():
        request.user.set_password(data['new_password'])
        request.user.save()
        delete_token(request.user)

    return generate_response(code=constans.ALL_OK, msg='重置密码成功,请重新登录')
