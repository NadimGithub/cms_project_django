from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None

        if username:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                print("User with this username does not exist.")
                # return None
                try:
                    user = UserModel.objects.get(email=username)
                except UserModel.DoesNotExist:
                    print("User with this email does not exist.")
                    try:
                        user = UserModel.objects.get(mobile=username)
                    except UserModel.DoesNotExist:
                        print("User with this mobile number does not exist.")
                        return None
        else:
            return None        
        if user is not None and user.check_password(password):
            return user
        print("Password is incorrect.")
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
