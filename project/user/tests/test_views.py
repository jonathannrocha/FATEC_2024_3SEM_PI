from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class UserTestCase(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            cpf='12345678901',
            gmail='teste@gmail.com',
            nome='Usuario Teste',
            password='senhaSegura123'
        )
        
    def test_login_success(self):
        response = self.client.post(reverse('login'), {'cpf': '12345678901', 'password': 'senhaSegura123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(self.client.session['_auth_user_id'])
    
    def test_login_no_success(self):
        response = self.client.post(reverse('login'), {'cpf': '1', 'password': '123'})        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'login')
