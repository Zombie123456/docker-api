from oauth2_provider.models import AccessToken

from rest_framework import renderers
from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail

from demo.lib import constans


def get_ip_addr(request):
    ipaddr = request.META.get('HTTP_MARTY_IP')
    if ipaddr:
        return ipaddr
    ipaddr = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ipaddr:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ipaddr = ipaddr.split(', ')[0]
    else:
        ipaddr = request.META.get('REMOTE_ADDR', '')

    return ipaddr


def get_user_type(user):
    if user:
        staff = user.staff_user
        if staff and staff.role:
            data = {
                'name': staff.role.name,
                'id': staff.role.id,
                'key': staff.role.key
            }
            return data
    return None


def parse_request_for_token(request):
    token = (request.META.get('HTTP_AUTHORIZATION') or '').split(' ')

    if len(token) < 2 or token[0] != 'Bearer':
        return None, None

    access_token = token[1]
    token_obj = AccessToken.objects.filter(token=access_token). \
        select_related('user').first()

    if not token_obj:
        return None, None

    user = token_obj.user

    if not user:
        return None, None

    user_group = (user.groups.filter(name='member_grp').first() or None)

    return user, user_group


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    try:
        if response.status_code in {400, 401, 404, 403, 405}:
            data_cpy = response.data.copy()
            error_list = []
            if isinstance(data_cpy, dict):
                for key, msg in data_cpy.items():
                    error_msg = msg
                    if isinstance(key, int) and isinstance(msg, list):
                        error_msg = msg[0]
                    elif key == 'error' or key == 'detail':
                        error_list.append(error_msg)
                        continue
                    error_list.append({key: error_msg})
            elif isinstance(data_cpy, list):
                error_list = response.data
            response.data = {'error': error_list}
    except Exception as exc:
        pass

    return response


class CampaignRenderer(renderers.JSONRenderer):
    def dict_error(self, data):
        error_list = []
        status = constans.NOT_OK
        for error in data.get('error'):
            if isinstance(error, ErrorDetail):
                error_msg = str(error).lower()
                for msg_code in constans.DRF_MESSAGES:
                    (code, msg), = msg_code.items()
                    if msg == error_msg:
                        status = code
                        break
            elif isinstance(error, dict):
                (k, v), = error.items()
                if isinstance(k, int):
                    status = k
                    error_msg = v
                else:
                    msg = v[0] if isinstance(v, list) else v
                    error_msg = f'{msg} : {k}'
            else:
                status = constans.NOT_OK_UNKNOWN
                error_msg = 'unknown error'
            error_list.append(error_msg)
        if len(error_list) > 1:
            status = constans.MULTIPLE_ERRORS
        return status, error_list, None

    def get_response_content(self, data, status_code):
        if 200 <= status_code < 300:
            # for success response, there still need to check partial success
            status = constans.ALL_OK
            msg = None
            content = data
        elif status_code in {400, 401, 404, 403, 405}:
            if isinstance(data, dict):
                status, msg, content = self.dict_error(data)
            elif isinstance(data, int):
                status = data
                msg = constans.ERROR_CODES.get(data, 'unknown error')
                content = None
            else:
                status = constans.NOT_OK
                msg = [data]
                content = None
        else:
            status = constans.NOT_OK_UNKNOWN
            msg = constans.ERROR_CODES.get(status)
            content = None
        response_content = {'code': status,
                            'msg': msg,
                            'data': content}
        return response_content

    def render(self, data, accepted_media_type=None, render_context=None):
        status_code = render_context['response'].status_code
        # if status code is not 200, this means the request has failed,
        # process it with corresponding custom payload
        response_content = self.get_response_content(data, status_code)
        # always set the response object's status code to 200
        render_context['response'].status_code = 200
        return super().\
            render(response_content, accepted_media_type, render_context)