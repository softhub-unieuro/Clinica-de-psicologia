"""
Decorators de segurança personalizados para o sistema.
Implementam verificações de permissão baseadas em cargo (RBAC).
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def cargo_required(*cargos_permitidos):
    """
    Decorator que restringe acesso baseado no cargo do usuário.
    
    Uso:
        @cargo_required('COORD', 'SUPER')
        def minha_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Você precisa estar autenticado.")
                return redirect('login')
            
            if request.user.cargo not in cargos_permitidos and not request.user.is_superuser:
                messages.error(
                    request, 
                    f"Acesso negado. Esta área é restrita a: {', '.join(cargos_permitidos)}"
                )
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def coordenador_required(view_func):
    """Decorator para views exclusivas do Coordenador."""
    return cargo_required('COORD')(view_func)


def supervisor_required(view_func):
    """Decorator para views exclusivas do Supervisor."""
    return cargo_required('SUPER')(view_func)


def estagiario_required(view_func):
    """Decorator para views exclusivas do Estagiário."""
    return cargo_required('ESTAG')(view_func)


def resp_tecnica_required(view_func):
    """Decorator para views exclusivas da Responsável Técnica."""
    return cargo_required('RESP_TEC')(view_func)


def staff_only(view_func):
    """Decorator para views acessíveis por qualquer staff (não pacientes)."""
    return cargo_required('COORD', 'SUPER', 'ESTAG', 'RESP_TEC', 'SEC')(view_func)
