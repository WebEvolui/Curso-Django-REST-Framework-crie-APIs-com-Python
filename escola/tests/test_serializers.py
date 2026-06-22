from django.test import TestCase
from escola.models import Estudante, Curso, Matricula
from escola.serializers import EstudanteSerializer, CursoSerializer, MatriculaSerializer

class EstudanteSerializerTestCase(TestCase):
    def setUp(self):
        self.estudante = Estudante(
            nome="João da Silva",
            email="joao@evolui.dev",
            cpf="68195899056",
            data_nascimento="2000-01-01",
            celular="11 99999-9999"
        )
        
        self.serializer_estudante = EstudanteSerializer(instance=self.estudante)
        
    def test_verifica_campos_serializados_estudante(self):
        """Teste para verificar se os campos do estudante foram serializados corretamente."""
        
        data = self.serializer_estudante.data
        self.assertEqual(set(data.keys()), set(['id', 'nome', 'email', 'cpf', 'data_nascimento', 'celular']))
    
    def test_verifica_valores_serializados_estudante(self):
        """Teste para verificar se os valores do estudante foram serializados corretamente."""
        
        data = self.serializer_estudante.data
        self.assertEqual(data['nome'], self.estudante.nome)
        self.assertEqual(data['email'], self.estudante.email)
        self.assertEqual(data['cpf'], self.estudante.cpf)
        self.assertEqual(data['data_nascimento'], str(self.estudante.data_nascimento))
        self.assertEqual(data['celular'], self.estudante.celular)

class CursoSerializerTestCase(TestCase):
    def setUp(self):
        self.curso = Curso(
            codigo="CS101",
            descricao="Evolui.dev - Cursos",
            nivel="B"
        )
        
        self.serializer_curso = CursoSerializer(instance=self.curso)
        
    def test_verifica_campos_serializados_curso(self):
        """Teste para verificar se os campos do curso foram serializados corretamente."""
        
        data = self.serializer_curso.data
        self.assertEqual(set(data.keys()), set(['id', 'codigo', 'descricao', 'nivel']))
    
    def test_verifica_valores_serializados_curso(self):
        """Teste para verificar se os valores do curso foram serializados corretamente."""
        
        data = self.serializer_curso.data
        self.assertEqual(data['codigo'], self.curso.codigo)
        self.assertEqual(data['descricao'], self.curso.descricao)
        self.assertEqual(data['nivel'], self.curso.nivel)

class MatriculaSerializerTestCase(TestCase):
    def setUp(self):
        self.estudante = Estudante(
            nome="João da Silva",
            email="joao@evolui.dev",
            cpf="68195899056",
            data_nascimento="2000-01-01",
            celular="11 99999-9999"
        )
        self.curso = Curso(
            codigo="CS101",
            descricao="Evolui.dev - Cursos",
            nivel="B"
        )
        self.matricula = Matricula(
            estudante=self.estudante,
            curso=self.curso
        )
        self.serializer_matricula = MatriculaSerializer(instance=self.matricula)
        
    def test_verifica_campos_serializados_matricula(self):
        """Teste para verificar se os campos da matrícula foram serializados corretamente."""
        
        data = self.serializer_matricula.data
        self.assertEqual(set(data.keys()), set(['id', 'estudante', 'curso', 'periodo']))
        
    def test_verifica_valores_serializados_matricula(self):
        """Teste para verificar se os valores da matrícula foram serializados corretamente."""
        
        data = self.serializer_matricula.data
        self.assertEqual(data['estudante'], self.matricula.estudante.id)
        self.assertEqual(data['curso'], self.matricula.curso.id)
        self.assertEqual(data['periodo'], self.matricula.periodo)
