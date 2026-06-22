from django.test import TestCase
from escola.models import Estudante

class EstudanteTestCase(TestCase):
    def teste_falha(self):
        self.fail("Teste de falha intencional para verificar o comportamento do teste.")