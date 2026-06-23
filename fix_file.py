# fix_encoding.py
with open('meu_banco.json', 'r', encoding='latin-1') as f:
    content = f.read()

with open('meu_banco_utf8.json', 'w', encoding='utf-8') as f:
    f.write(content)
    

# python manage.py dumpdata auth.user auth.permission contenttypes.contenttype escola.estudante escola.curso escola.matricula --output meu_banco.json --indent 2