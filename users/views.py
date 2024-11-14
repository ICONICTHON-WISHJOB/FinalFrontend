from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer
from .models import CustomUser, Company


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')  # Assuming the identifier for both users is 'user_id'
        password = request.data.get('password')

        # Attempt to authenticate as CustomUser first
        user = authenticate(username=user_id, password=password)
        if user is not None and isinstance(user, CustomUser):
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key,
                "user_type": 0
            }, status=status.HTTP_200_OK)

        # Attempt to authenticate as Company if CustomUser failed
        try:
            company = Company.objects.get(company_id=user_id)
            if company.check_password(password):
                return Response({
                    "message": "Login successful",
                    "user_type": 1
                }, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            pass

        # If authentication fails
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

