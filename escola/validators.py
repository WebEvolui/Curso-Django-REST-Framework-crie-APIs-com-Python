import re
from validate_docbr import CPF 

def cpf_invalido(value):
    cpf = CPF()
    return not cpf.validate(value)

def nome_invalido(nome):
    return not nome.isalpha()

def celular_invalido(celular):
    # padrão esperado: 33 99999-8888 (13 caracteres, incluindo espaço e hífen)
    padrao = '[0-9]{2} [0-9]{5}-[0-9]{4}'
    return not re.findall(padrao, celular)