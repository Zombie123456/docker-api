from django.utils.translation import ugettext_lazy as _


ALL_OK = 2000
AUTH_CREDENTIALS_NOT_FOUND = 9007
NOT_OK_UNKNOWN = 9008
NOT_ALLOWED = 7001
NOT_OK = 9009
MULTIPLE_ERRORS = 9010
FIELD_ERROR = 9011
REQUIRED_FIELD = 9012
NO_ENVELOPE = 4008
ATLEAST_ONE_FIELD = 9013

# MESSAGES from DRF
# (RESPONSE_CODE, SPECIFIC MESSAGE, Commonalised?)
DRF_MESSAGES = (
    {4011: _('you do not have permission to perform this action.')},
    {4010: _('invalid authorization header. credentials string should not contain spaces')},
    {4010: _('authentication credentials were not provided.')},
    {4010: _('error decoding signature')},
    {4010: _('signature has expired')},
    {7001: _('method "put" not allowed.')},
    {7001: _('method "post" not allowed.')},
    {7001: _('method "patch" not allowed.')},
    {7001: _('method "delete" not allowed.')},
    {7001: _('method "get" not allowed.')},
)

ERROR_CODES = {
    NOT_OK_UNKNOWN: _('未知错误'),
    NO_ENVELOPE: _('红包活动没有开启')
}


# COMMON CODES
EXPIRED_TOKEN = 9006
NOT_OK_UNKNOWN = 9008
INVALID_CAPTCHA = 9013
ACTION_TOO_FREQUENT = 9014
MEMBER_NOT_FOUND = 1001


# ACCOUNT RELATED
USERNAME_IN_USED = 1004
INVALID_USERNAME = 1011


