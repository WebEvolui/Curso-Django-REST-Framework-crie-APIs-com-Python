from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status
from escola.models import Curso


class CursosTestCase(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_superuser(username="admin", password="admin")
        self.url = reverse("Cursos-list", kwargs={"version": "v1"})
        self.client.force_authenticate(user=self.usuario)
        self.curso_1 = Curso.objects.create(
            codigo="CS101",
            descricao="Cursos em Evolui.dev",
            nivel="B",
        )

    def test_listar_cursos(self):
        """Testa se a listagem de cursos retorna o status code 200 OK."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
