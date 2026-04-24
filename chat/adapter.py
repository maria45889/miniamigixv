from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from allauth.account.utils import perform_login

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return '/'

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Si el usuario ya existe en redes sociales, no hacemos nada
        if sociallogin.is_existing:
            return

        # Si no existe, intentamos conectarlo por correo
        user_model = get_user_model()
        email = sociallogin.user.email
        if email:
            try:
                user = user_model.objects.get(email=email)
                sociallogin.connect(request, user)
            except user_model.DoesNotExist:
                pass
