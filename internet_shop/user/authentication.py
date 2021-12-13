import re

from .models import User


class UserAuthBackend(object):

    def authenticate(self, request, username=None, password=None):
        if re.search('[0-9a-z]+@[a-z.]+', username):
            kwargs = {'email': username}
        else:
            kwargs = {'phone': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
