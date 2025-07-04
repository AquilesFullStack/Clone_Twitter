from rest_framework import serializers
from .models import User 
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)#criado manualemente 
    #write_only = somente ser enviado
    
    class Meta:
        model = User #conectado com o modelo USER
        fields = ['username', 'email', 'password'] #vai manipular os campos
        
    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')
        
        if not username.isalnum():
            raise serializers.ValidationError('O usuário deve ter apenas caracteres alfanuméricos')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    
    class Meta: 
        model = User
        fields = ['token']
        
        
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=3)
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    username=serializers.EmailField(max_length=255, min_length=3, read_only=True)
    tokens=serializers.SerializerMethodField()
    
    def get_tokens(self,obj):
        user = User.objects.get(email=obj['email'])
        return {'access': user.tokens()['access'],
                'refresh': user.tokens()['refresh']}
    
    class Meta:
        model = User
        fields = ['email', 'password','username', 'tokens']
    
    def validate(self, attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')
        
        user = auth.authenticate(email=email, password=password)
        if not user: 
            raise AuthenticationFailed('Credenciais inválidas, tente novamente')    
        if not user.is_active: 
            raise AuthenticationFailed('Conta desativada, contate o administrador')
        if not user.is_verified:
            raise AuthenticationFailed('Email não foi verificado')
        
        return{
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
        

class RequestPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
        
    class Meta: 
        fields = ['email']
        
class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=6, max_length=68, write_only=True)
    token=serializers.CharField(min_length=1, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)
    
    class Meta:
        fields = ['password', 'token', 'uidb64']
        
        def validate(self, attrs):
            try: 
                password = attrs.get('password')
                token= attrs.get('token')
                uidb64=attrs.get('uidb64')
                
                id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=id)
                
                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise AuthenticationFailed('Link de reset é inválido', 401)
                
                user.set_password(password)
                user.save()
                
                return (user)
            except Exception as e:
                raise AuthenticationFailed('Link de reset é inválido', 401)
            return super().validate(attrs)