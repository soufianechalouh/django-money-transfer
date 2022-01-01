from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, views
from .serializers import RegisterSerializer, EmailValidationSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = self.serializer_class(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()

        user_data = user.data
        user = User.objects.get(email=user_data["email"])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        abs_url = "http://" + current_site + relative_link + "?token=" + str(token)
        email_body = "Hi " + user.username + ", Use link bellow to verify your emai \n" + abs_url
        data = {"email_body": email_body, "to": user.email, "email_subject": "Verify your account",
                "domain": current_site}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailValidationSerializer

    def get(self, request):
        token = request.GET.get("token")

        try:

            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"email": "Successfully activated"}, status=status.HTTP_201_CREATED)

        except jwt.ExpiredSignatureError as expired:
            return Response({"error": "Activation expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"error": "Invalid token, request a new one"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error", f"Unexpected error {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
