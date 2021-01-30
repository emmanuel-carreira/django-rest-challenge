from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, status, views
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserModelSerializer, UserLoginSerializer
from .utils import get_token_for_user


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserModelSerializer

    def post(self, request):
        data = request.data
        data['first_name'] = data.pop('firstName', '')
        data['last_name'] = data.pop('lastName', '')

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            token = get_token_for_user(user)
            response_data = {
                'user': serializer.data,
                'token': token
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        error = serializer.errors.get('non_field_errors')
        if not error:
            error = serializer.errors.get('phones')[0].get('non_field_errors')

        response_data = {
            'message': error,
            'errorCode': 400
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)

        error = serializer.errors.get('non_field_errors')
        response_data = {
            'message': error,
            'errorCode': 400
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserModelSerializer

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            response_data = {'message': 'Unauthorized', 'errorCode': 401}
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user, token = JWTAuthentication().authenticate(request)
        except:
            response_data = {
                'message': 'Unauthorized - invalid session',
                'errorCode': 401
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(user)
        response_data = {'user': serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

