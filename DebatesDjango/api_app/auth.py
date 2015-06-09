# Authenticate request coming from Sproxy

from django.contrib.auth.models    import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions     import AuthenticationFailed

class SproxyAuth(BaseAuthentication):
    def authenticate(self, request):
        header = request.META
        username = header.get('HTTP_FROM')
        if username == None:
            msg = "Could not find 'HTTP_FROM' field in header:\n" + str(header)
            raise AuthenticationFailed(msg)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            msg = "Could not find user with username: " + username
            raise AuthenticationFailed(msg)
        if user.get('first_name') == None:
            user['first_name'] = header.get('HTTP_X_GIVEN_NAME')
        if user.get('last_name') == None:
            user['last_name'] = header.get('HTTP_X_FAMILY_NAME')
        return user
