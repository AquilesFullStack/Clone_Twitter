from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializer import PostsSerializer
from .models import Posts
from rest_framework import permissions
from .permissions import IsOwner #garante que o usuário só ver o que for dele

class PostsListAPIView(ListCreateAPIView): #lista GET e cria POST
    serializer_class = PostsSerializer #converte e valida como base
    queryset = Posts.objects.all() #filtra por usuário
    permission_classes = (permissions.IsAuthenticated,) #permite acesso somente à autenticados
    
    #quando um POST for feito salva o owner automaticamente como o usuário que está autenticado
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    #busca os posts e trás só o que pertence à ele, aqui um usuário não vê o post do outro
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    

class PostDetailAPIView(RetrieveUpdateDestroyAPIView): #permite ver GET, atualizat PUT/PATCH e deletar DELETE
    
    #exige que o usuário esteja autenticado e seja o dono do post
    serializer_class = PostsSerializer
    permission_classes = [IsOwner]
    queryset = Posts.objects.all()
    
    #toda busca será feita pelo ID 
    lookup_field = "id"
    
    #busca os posts e trás só o que pertence à ele, aqui um usuário não vê o post do outro
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)