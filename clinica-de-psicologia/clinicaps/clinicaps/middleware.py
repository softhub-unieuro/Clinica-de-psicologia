"""
Middleware customizado para auditoria de acessos (LGPD)
Este middleware registra acessos a dados sensíveis SEM ARMAZENAR OS DADOS EM SI.
"""
import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger('django.security')

class AuditMiddleware(MiddlewareMixin):
    """
    Middleware de auditoria para conformidade com LGPD.
    Registra acessos a dados sensíveis sem expor os dados em logs.
    """
    
    SENSITIVE_PATHS = [
        '/estagiario/consulta-inscritos/',
        '/estagiario/dados-inscrito/',
        '/coordenador/',
        '/supervisor/',
        '/resptecn/',
    ]
    
    def process_request(self, request):
        """
        Registra tentativas de acesso a áreas sensíveis.
        IMPORTANTE: NÃO registra dados pessoais, apenas metadados.
        """
        user = request.user
        path = request.path
        
        # Verifica se é uma área sensível
        if any(path.startswith(sensitive) for sensitive in self.SENSITIVE_PATHS):
            if isinstance(user, AnonymousUser):
                logger.warning(
                    f"Tentativa de acesso não autenticado a área sensível: {path}"
                )
            else:
                logger.info(
                    f"Acesso a área sensível - Usuário: {user.matricula} "
                    f"(Cargo: {user.cargo}) - Path: {path} - IP: {self.get_client_ip(request)}"
                )
        
        return None
    
    def get_client_ip(self, request):
        """Obtém o IP do cliente de forma segura."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
