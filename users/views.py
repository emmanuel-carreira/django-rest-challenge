from rest_framework.response import Response
from rest_framework import generics, status

from .serializers import ProfileSerializer


class ProfileCreateView(generics.CreateAPIView):
    serializer_class = ProfileSerializer

    def post(self, request):
        data = request.data
        data['first_name'] = data.pop('firstName', '')
        data['last_name'] = data.pop('lastName', '')

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        error = serializer.errors.get('non_field_errors')
        if not error:
            error = serializer.errors.get('phones')[0].get('non_field_errors')

        json_error = {"message": error, "errorCode": 400}
        return Response(json_error, status=status.HTTP_400_BAD_REQUEST)
