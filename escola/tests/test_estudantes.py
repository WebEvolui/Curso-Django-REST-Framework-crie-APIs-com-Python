from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status
from escola.models import Estudante


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
