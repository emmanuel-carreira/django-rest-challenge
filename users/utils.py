from rest_framework_simplejwt.tokens import AccessToken


def get_token_for_user(user):
    access_token = AccessToken.for_user(user)
    return str(access_token)


def format_data(data):
    data['firstName'] = data.pop('first_name', '')
    data['lastName'] = data.pop('last_name', '')
    return data
