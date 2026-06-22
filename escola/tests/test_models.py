from django.test import TestCase
from escola.models import Curso, Estudante, Matricula


class ModelEstudanteTestCase(TestCase):
    def setUp(self):
        self.estudante = Estudante.objects.create(
            nome="João da Silva",
            email="joao@example.com",
            cpf="68195899056",
            data_nascimento="2000-01-01",
            celular="11 99999-9999",
        )
        
    def test_verificar_estudante(self):
        """Teste para verificar se o estudante foi criado corretamente."""
        
        self.assertEqual(self.estudante.nome, "João da Silva")
        self.assertEqual(self.estudante.email, "joao@example.com")
        self.assertEqual(self.estudante.cpf, "68195899056")
        self.assertEqual(self.estudante.data_nascimento, "2000-01-01")
        self.assertEqual(self.estudante.celular, "11 99999-9999")
        
        
class ModelCursoTestCase(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            codigo="CS101",
            descricao="Evolui.dev - Cursos",
            nivel="B"
        )
        
    def test_verificar_curso(self):
        """Teste para verificar se o curso foi criado corretamente."""
        
        self.assertEqual(self.curso.codigo, "CS101")
        self.assertEqual(self.curso.descricao, "Evolui.dev - Cursos")
        self.assertEqual(self.curso.nivel, "B")
        

class ModelMatriculaTestCase(TestCase):
    def setUp(self):
        self.estudante = Estudante.objects.create(
            nome="João da Silva",
            email="joao@example.com",
            cpf="68195899056",
            data_nascimento="2000-01-01",
            celular="11 99999-9999"
        )
        self.curso = Curso.objects.create(
            codigo="CS101",
            descricao="Evolui.dev - Cursos",
            nivel="B"
        )
        self.matricula = Matricula.objects.create(
            estudante=self.estudante,
            curso=self.curso,
            periodo="M"
        )
        
    def test_verificar_matricula(self):
        """Teste para verificar se a matrícula foi criada corretamente."""
        
        self.assertEqual(self.matricula.estudante.nome, "João da Silva")
        self.assertEqual(self.matricula.curso.descricao, "Evolui.dev - Cursos")
        self.assertEqual(self.matricula.periodo, "M")   