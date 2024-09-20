from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            cpf='12345678901',
            senha='senha_secreta',
            nome='Teste Usuário',
            gmail='teste@teste.com'
        )

    def test_user_login_valid(self):
        response = self.client.post(reverse('user_login'), {
            'cpf': '12345678901',
            'senha': 'senha_secreta'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_user_login_invalid(self):
        response = self.client.post(reverse('user_login'), {
            'cpf': '12345678901',
            'senha': 'senha_errada'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CPF ou senha inválidos.')

    def test_cadastrar_usuario(self):
        response = self.client.post(reverse('cadastrarUsuario'), {
            'nome': 'Novo Usuário',
            'cpf': '98765432100',
            'gmail': 'novo@teste.com',
            'telefone': '123456789',
            'senha': 'nova_senha',
            'dataNascimento': '2000-01-01',
            'typeUser': 'mentorado'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        novo_user = self.User.objects.get(cpf='98765432100')
        self.assertIsNotNone(novo_user)


    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index1.html')

    def test_dashboard_view_authenticated(self):
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard1.html')

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('user_login')}?next={reverse('dashboard')}")

    def test_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_login'))
