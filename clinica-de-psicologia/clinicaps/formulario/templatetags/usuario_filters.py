# formulario/templatetags/usuario_filters.py
from django import template
import re

register = template.Library()

@register.filter
def censurar_cpf(cpf):
    """
    Censura CPF mostrando apenas os 3 dígitos do meio
    Uso: {{ cpf|censurar_cpf }}
    """
    if not cpf:
        return "CPF não informado"
    
    # Converte para string
    cpf_str = str(cpf)
    
    # Remove tudo que não é número (pontos, traços, espaços)
    apenas_numeros = re.sub(r'\D', '', cpf_str)
    
    # Verifica se tem 11 dígitos
    if len(apenas_numeros) == 11:
        # Pega os 3 dígitos do meio (índices 4, 5, 6 - posições 5, 6, 7)
        meio = apenas_numeros[4:7]  # 5º, 6º e 7º dígitos
        # Retorna com máscara mostrando apenas os 3 do meio
        return f"***.{meio}.***-**"
    elif len(apenas_numeros) >= 3:
        # Caso não tenha 11 dígitos, mostra os 3 primeiros ou do meio disponíveis
        meio = apenas_numeros[4:7] if len(apenas_numeros) > 4 else apenas_numeros[:3]
        return f"***.{meio}.***-**"
    else:
        # Se o CPF tiver menos de 3 números, retorna só asteriscos
        return "***.***.***-**"