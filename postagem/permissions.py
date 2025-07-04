#impede que uum usuário edite ou apague um post que não o pertence

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        #permite apenas leitura para os métodos em SAFE_METHODS
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user    