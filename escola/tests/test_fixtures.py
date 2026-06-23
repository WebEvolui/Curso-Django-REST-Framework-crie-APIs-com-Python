from django.test import TestCase
from escola.models import Estudante, Curso

class FixturesTestCase(TestCase):
    fixtures = ['meu_banco_utf8.json']
    
    def test_carregamento_da_fixtures(self):
        estudante = Estudante.objects.get(cpf='33359999401')
        curso = Curso.objects.get(codigo='CDJRF04')
        self.assertEqual(estudante.email, 'anabeatrizlima@live.com')
        self.assertEqual(curso.descricao, 'Curso de Django REST Framework 04')
