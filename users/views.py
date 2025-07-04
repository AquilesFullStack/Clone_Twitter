from django.shortcuts import render 
from rest_framework import generics, status, views
from .serializers import RegisterSerializer, RequestPasswordEmailRequestSerializer, EmailVerificationSerializer, LoginSerializer, SetNewPasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, force_bytes ,DjangoUnicodeDecodeError 
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util


class RegisterView(generics.GenericAPIView): #genericAPIView tem coisas prontas: pega requisição, gerencia validação...
    
    serializer_class = RegisterSerializer #quando a view for chamada vai usar o registerSerialize para validar e tratar os dados
    renderer_classes = (UserRenderer,)
    
    def post(self, request): #método chamado quando chega uma requisição POST
        user = request.data #coleta os dados que o cliente enviou em JSON
        serializer = self.serializer_class(data=user) #cria uma instância do RegisteSerializer passando os dados para ele validar
        serializer.is_valid(raise_exception=True) #valida se está correto, se não retorna 400
        serializer.save() #se os dados estiverem corretos, salva no DB
        user_data = serializer.data #coleta os dados serializados
        
        user = User.objects.get(email=user_data['email']) # consulta o banco pelo email
        token = RefreshToken.for_user(user).access_token #gera um token de longa duração
        
        current_site = get_current_site(request).domain #pega o dominio da requisição
        relativeLink = reverse('email-verify')
        
        absurl ='https://' + current_site + relativeLink + "?token=" + str(token)
        email_body= 'Olá' +user.username + 'use o link abaixo para verificar seu email \n' + absurl
        data = {'to_email':user.email, 'email_body': email_body, 'email_subject':'Verifique seu email','domain': absurl} #dicionario para enviar mensagem mt provavelmente
        Util.send_email(data) #envia email 
        
        return Response(user_data, status=status.HTTP_201_CREATED) #retorna os dados que acabou de ser criado
    
    
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Descrição', type=openapi.TYPE_STRING
    )
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Ativado com Sucesso'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier: 
            return Response({'error':'Ativação expirada'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier: 
            return Response({'error':'Token Inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginApiView(generics.CreateAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RequestPasswordResetEmail(generics.CreateAPIView):
    serializer_class = RequestPasswordEmailRequestSerializer
    
    def post(self, request):
        # data = {'request': request , 'data': request.data}
        serializer = self.serializer_class(data=request.data)
        
        email = request.data['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain #pega o dominio da requisição
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl ='https://' + current_site + relativeLink
            email_body= 'Olá \n use o link abaixo para resetar sua senha \n' + absurl
            data = {'to_email':user.email, 'email_body': email_body, 'email_subject':'Resete sua senha','domain': absurl} #dicionario para enviar mensagem mt provavelmente
            Util.send_email(data) #envia email 
        return Response({'success': 'Enviamos o link para resetar sua senha'}, status=status.HTTP_200_OK)
        
class PasswordTokenCheckAPI(generics.GenericAPIView): 
    serializer_class= SetNewPasswordSerializer
    def get(self, request, uidb64, token):
        try: 
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token não é válido, tente novamente'})
            
            return Response({'success': True, 'message':'Credenciais válidas', 'uidb64': uidb64, 'token': token})
        
        except DjangoUnicodeDecodeError as identifier: 
            if PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token não é valido, tente novamente'}) 

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'success':True, 'mensagem':'Senha resetada com sucesso'}, status=status.HTTP_200_OK
        )