"""
Utilitários para criptografia e anonimização de dados (LGPD).
ATENÇÃO: Para dados verdadeiramente sensíveis em produção, considere 
usar bibliotecas especializadas como django-fernet-fields ou cryptography.
"""
import hashlib
from django.conf import settings


def hash_cpf(cpf):
    """
    Cria um hash irreversível do CPF para comparações.
    Útil para busca sem expor o CPF completo nos logs.
    
    Args:
        cpf (str): CPF a ser hasheado
    
    Returns:
        str: Hash SHA256 do CPF
    """
    if not cpf:
        return None
    
    # Adiciona salt usando SECRET_KEY para aumentar segurança
    salt = settings.SECRET_KEY.encode()
    cpf_bytes = cpf.encode()
    
    return hashlib.sha256(salt + cpf_bytes).hexdigest()


def mascarar_cpf(cpf):
    """
    Mascara CPF para exibição segura (LGPD).
    
    Exemplo: 123.456.789-00 -> ***.456.789-**
    
    Args:
        cpf (str): CPF a ser mascarado
    
    Returns:
        str: CPF mascarado
    """
    if not cpf or len(cpf) < 11:
        return "***.***.***-**"
    
    # Remove caracteres não numéricos
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    
    # Formata com máscara
    return f"***.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-**"


def mascarar_email(email):
    """
    Mascara email para exibição segura (LGPD).
    
    Exemplo: usuario@exemplo.com -> u***o@e***o.com
    
    Args:
        email (str): Email a ser mascarado
    
    Returns:
        str: Email mascarado
    """
    if not email or '@' not in email:
        return "***@***.***"
    
    partes = email.split('@')
    usuario = partes[0]
    dominio = partes[1]
    
    # Mascara usuário (primeira e última letra)
    if len(usuario) > 2:
        usuario_mascarado = usuario[0] + '*' * (len(usuario) - 2) + usuario[-1]
    else:
        usuario_mascarado = '*' * len(usuario)
    
    # Mascara domínio
    partes_dominio = dominio.split('.')
    if len(partes_dominio[0]) > 2:
        dominio_mascarado = partes_dominio[0][0] + '*' * (len(partes_dominio[0]) - 2) + partes_dominio[0][-1]
    else:
        dominio_mascarado = '*' * len(partes_dominio[0])
    
    dominio_final = dominio_mascarado + '.' + '.'.join(partes_dominio[1:])
    
    return f"{usuario_mascarado}@{dominio_final}"


def mascarar_telefone(telefone):
    """
    Mascara telefone para exibição segura (LGPD).
    
    Exemplo: (61) 98765-4321 -> (61) ****-4321
    
    Args:
        telefone (str): Telefone a ser mascarado
    
    Returns:
        str: Telefone mascarado
    """
    if not telefone:
        return "(**) ****-****"
    
    # Remove caracteres não numéricos
    tel_limpo = ''.join(filter(str.isdigit, telefone))
    
    if len(tel_limpo) >= 10:
        ddd = tel_limpo[:2]
        sufixo = tel_limpo[-4:]
        return f"({ddd}) ****-{sufixo}"
    
    return "(**) ****-****"


def sanitizar_log_message(message):
    """
    Remove ou mascara dados sensíveis de mensagens de log (LGPD).
    
    Args:
        message (str): Mensagem original
    
    Returns:
        str: Mensagem sanitizada
    """
    import re
    
    # Mascara CPFs no formato XXX.XXX.XXX-XX
    message = re.sub(
        r'\d{3}\.\d{3}\.\d{3}-\d{2}',
        '***.***.***-**',
        message
    )
    
    # Mascara CPFs no formato XXXXXXXXXXX
    message = re.sub(
        r'\b\d{11}\b',
        '***********',
        message
    )
    
    # Mascara emails
    message = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '***@***.***',
        message
    )
    
    # Mascara telefones
    message = re.sub(
        r'\(\d{2}\)\s?\d{4,5}-?\d{4}',
        '(**) ****-****',
        message
    )
    
    return message
