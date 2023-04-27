from django.conf import settings
from rest_framework.authtoken.models import Token
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .tokens import create_jwt_pair_for_user
from . models import User
from user_profile.models import OwnerProfile
from . permission import IsOwnerOrReadObly
from rest_framework.decorators import api_view
from user_profile.models import  OwnerProfile
from django.shortcuts import render, redirect, HttpResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, mixins
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from .serializers import OwnerRegisterSerializer, OwnerSerializer, LoginSerializer
import google.auth.transport.requests
import google.oauth2.id_token
from rest_framework.decorators import permission_classes,renderer_classes
from rest_framework.response import Response
from google.oauth2.credentials import Credentials
from django.views import View
from django.http import JsonResponse
import requests
from django.middleware.csrf import get_token
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.renderers import JSONRenderer,TemplateHTMLRenderer
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.

class OwnerRegisterView(generics.CreateAPIView):

    serializer_class = OwnerRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Owner Profile Created Successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        response = {
            "message": serializer.errors
        }

        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class OwnerListView(generics.ListAPIView):
    serializer_class = OwnerSerializer
    queryset = OwnerProfile.objects.all()
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, format=None):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            tokens = create_jwt_pair_for_user(user)
            Token.objects.get_or_create(tokens)
            response = {
                'message': "Login Successfully",
                "Token": tokens
            }


            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request):
        response = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=response, status=status.HTTP_200_OK)


class User_logout(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes=[]
    def get(self, request: Request,  format=None):
        logout(request)
        response = {
            "message": "Logout Successfully"
        }
        return Response(data=response, status=status.HTTP_200_OK)


from google.oauth2 import id_token
from google.auth.transport import requests
import json
from ast import literal_eval
import jwt
@api_view(('POST',))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes([AllowAny])
def handleGoogleAuthSignin(request):
    form_data = request.body
    body=literal_eval(form_data.decode('utf-8'))
    s = json.dumps(body, indent=4, sort_keys=True)
    print(s)
    token = body.get('id_token')
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        print(id_token)
        print(settings.GOOGLE_OAUTH_CLIENT_ID)
        print(token)
        idinfo = id_token.verify_oauth2_token(token,requests.Request(),settings.GOOGLE_OAUTH_CLIENT_ID)
        print("id_info:",idinfo)
        # ID token is valid.Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        print("userId:",userid)
        if User.objects.filter(email=idinfo['email'], account_type='google').exists() and User.objects.filter(email=idinfo['email'], account_type='google'):
            user = User.objects.get(email=idinfo['email']).pk
            login(request, user)
            # tokens = create_jwt_pair_for_user(user)
            Token.objects.get_or_create(token)
            response = {
                'message': "Login Successfully",
                "Token": token
            }
            print(response)
            return response
        else:
            messagePoint = {'status': 'error', 'msg': 'Unknown user' }
            return Response(messagePoint)
    except Exception as e:
        print(e)
        # Invalid token
        messagePoint = {'status': 'error', 'msg': 'Unknown user' }
        return Response(messagePoint)