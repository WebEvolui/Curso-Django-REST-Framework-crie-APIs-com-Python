from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status
from escola.models import Curso
from escola.serializers import CursoSerializer


class CursosTestCase(APITestCase):
    fixtures = ["meu_banco_utf8.json"]

    def setUp(self):
        self.usuario = User.objects.get(username="admin")
        self.url = reverse("Cursos-list", kwargs={"version": "v1"})
        self.client.force_authenticate(user=self.usuario)
        self.curso_1 = Curso.objects.get(pk=1)

    def test_listar_cursos(self):
        """Testa se a listagem de cursos retorna o status code 200 OK."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listar_um_curso(self):
        """Testa se a listagem de um curso específico retorna o status code 200 OK."""
        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dados_curso = Curso.objects.get(pk=1)
        dados_serializados = CursoSerializer(instance=dados_curso).data
        self.assertEqual(response.data, dados_serializados)

    def test_post_curso(self):
        """Testa se a criação de um curso retorna o status code 201 Created."""
        data = {"codigo": "CS102", "descricao": "Curso de Teste", "nivel": "B"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_curso(self):
        """Testa se a exclusão de um curso retorna o status code 204 No Content."""
        response = self.client.delete(f"{self.url}1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_curso(self):
        """Testa se a atualização de um curso retorna o status code 200 OK."""
        data = {
            "codigo": "CS101",
            "descricao": "Curso de Teste Atualizado",
            "nivel": "B",
        }
        response = self.client.put(f"{self.url}1/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Curso.objects.get(pk=1).descricao, "Curso de Teste Atualizado")
