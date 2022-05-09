
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserLoginSerializer


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            # 'iin': user.iin,
            # 'name': user.name
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class Blocked(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = {
            'ok': 'ok',
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)
