from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate

class AuthUserTestCase(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_superuser(username='admin', password='admin')
        
    def test_auth_user_ok(self):
        """Testa se o usuário é autenticado corretamente com as credenciais fornecidas."""
        
        user = authenticate(username='admin', password='admin')
        self.assertTrue((user is not None) and (user.is_authenticated))
        
    def test_auth_username_incorreto(self):
        """Testa se o usuário não é autenticado com nome de usuário incorreto."""
        
        user = authenticate(username='invaliduser', password='admin')
        self.assertFalse((user is not None) and (user.is_authenticated))
        
    def test_auth_password_incorreto(self):
        """Testa se o usuário não é autenticado com senha incorreta."""
        
        user = authenticate(username='admin', password='invalidpassword')
        self.assertFalse((user is not None) and (user.is_authenticated))
