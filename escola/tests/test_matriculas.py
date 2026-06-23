from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status
from escola.models import Matricula, Estudante, Curso
from escola.serializers import MatriculaSerializer


class MatriculasTestCase(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_superuser(username="admin", password="admin")
        self.url = reverse("Matriculas-list", kwargs={"version": "v1"})
        self.client.force_authenticate(user=self.usuario)
        self.estudante = Estudante.objects.create(
            nome="João",
            email="joao@evolui.dev",
            cpf="74464601057",
            data_nascimento="2000-01-01",
            celular="11 99999-9999",
        )
        self.curso = Curso.objects.create(
            codigo="CS101",
            descricao="Curso de Teste",
            nivel="B",
        )
        self.curso_2 = Curso.objects.create(
            codigo="CS102",
            descricao="Curso de Teste 2",
            nivel="B",
        )
        self.matricula = Matricula.objects.create(
            estudante=self.estudante,
            curso=self.curso,
            periodo="M",
        )

    def test_listar_matriculas(self):
        """Testa se a listagem de matrículas retorna o status code 200 OK."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        
    def test_listar_uma_matricula(self):
        """Testa se a listagem de uma matrícula específica retorna o status code 200 OK."""
        response = self.client.get(self.url+'1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dados_matricula = Matricula.objects.get(pk=1)
        dados_serializados = MatriculaSerializer(instance=dados_matricula).data
        self.assertEqual(response.data, dados_serializados)
        
    def test_post_matricula(self):
        """Testa se a criação de uma matrícula retorna o status code 201 Created."""
        data = {
            "estudante": self.estudante.id,
            "curso": self.curso_2.id,
            "periodo": "M"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Matricula.objects.count(), 2)
        self.assertEqual(Matricula.objects.get(pk=2).estudante.nome, "João")    
        self.assertEqual(Matricula.objects.get(pk=2).curso.codigo, self.curso_2.codigo)
        
    def test_delete_matricula(self):
        """Testa se a exclusão de uma matrícula retorna o status code 204 No Content."""
        response = self.client.delete(f"{self.url}1/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_put_matricula(self):
        """Testa se a atualização de uma matrícula retorna o status code 405 Method Not Allowed."""
        data = {
            "estudante": self.estudante.id,
            "curso": self.curso.id,
            "periodo": "V"
        }
        response = self.client.put(f"{self.url}1/", data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
