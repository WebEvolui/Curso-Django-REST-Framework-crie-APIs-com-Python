from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status
from escola.models import Estudante
from escola.serializers import EstudanteSerializer


class EstudantesTestCase(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_superuser(username="admin", password="admin")
        self.url = reverse("Estudantes-list", kwargs={"version": "v1"})
        self.client.force_authenticate(user=self.usuario)
        self.estudante_1 = Estudante.objects.create(
            nome="João",
            email="joao@evolui.dev",
            cpf="74464601057",
            data_nascimento="2000-01-01",
            celular="11 99999-9999",
        )
        self.estudante_2 = Estudante.objects.create(
            nome="Maria",
            email="maria@evolui.dev",
            cpf="80423650041",
            data_nascimento="2000-01-01",
            celular="11 99999-9999",
        )

    def test_listar_estudantes(self):
        """Testa se a listagem de estudantes retorna o status code 200 OK."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_listar_um_estudante(self):
        """Testa se a listagem de um estudante específico retorna o status code 200 OK."""
        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dados_estudante = Estudante.objects.get(pk=1)
        dados_serializados = EstudanteSerializer(instance=dados_estudante).data
        self.assertEqual(response.data, dados_serializados)

    def test_post_estudante(self):
        """Testa se a criação de um estudante retorna o status code 201 Created."""
        data = {
            "nome": "Carlos",
            "email": "carlos@evolui.dev",
            "cpf": "34373319065",
            "data_nascimento": "2000-01-01",
            "celular": "11 99999-9999",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Estudante.objects.count(), 3)
        self.assertEqual(Estudante.objects.get(pk=3).nome, "Carlos")

    def test_delete_estudante(self):
        """Testa se a exclusão de um estudante retorna o status code 204 No Content."""
        response = self.client.delete(f"{self.url}2/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_estudante(self):
        """Testa se a atualização de um estudante retorna o status code 200 OK."""
        data = {
            "nome": "Joao Silva",
            "email": "joaoput@evolui.dev",
            "cpf": "74012667092",
            "data_nascimento": "2000-01-01",
            "celular": "11 11111-2222",
        }
        response = self.client.put(f"{self.url}1/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
