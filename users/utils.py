from rest_framework_simplejwt.tokens import AccessToken

def get_token_for_profile(profile):
    access_token = AccessToken.for_user(profile)
    return str(access_token)
