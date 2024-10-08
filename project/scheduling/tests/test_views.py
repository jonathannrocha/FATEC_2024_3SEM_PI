from django.test import TestCase, Client
from user.models import Perfil, User
from mongoengine import connect, disconnect
from datetime import datetime
from django.urls import reverse

class ViewsTestCase(TestCase):
    def setUp(self):
        disconnect(alias='default')
        connect('testdb', alias='default')
        Perfil.drop_collection()

        self.perfil = Perfil(
            cpf="1234567801",
            nome="Teste",
            sobre="Descrição do mentor",
            nivelExperiencia="Intermediário",
            nivel="Nível 1",
            certificacoes=["Certificado A", "Certificado B"],
            habilidades=["Python", "Django"],
            redesSociais=["LinkedIn", "GitHub"],
            horariosDisponiveis=[
                datetime.fromisoformat("2024-10-05T10:00:00"),
                datetime.fromisoformat("2024-10-06T14:00:00")
            ]
        )
        self.perfil.save()
        self.mentorado = User.objects.create_user(
            cpf="12345678901",
            senha="senha123",
            nome="Mentorado Teste",
            gmail="mentorado@teste.com",
            typeUser="mentorado"
        )

        self.client = Client()

    def tearDown(self):
        disconnect(alias='default')

    def test_viewHorarios(self):
        response = self.client.get(reverse('viewHorarios', args=[self.perfil.cpf]))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_horarios = [
            "2024-10-05T10:00:00",
            "2024-10-06T14:00:00"
        ]
        actual_horarios = [datetime.fromisoformat(h).isoformat() for h in response_data['horariosDisponiveis']]
        self.assertListEqual(expected_horarios, actual_horarios)
    def test_marcarMentoria(self):
        self.client.login(cpf="12345678901", password="senha123")
        response = self.client.post(reverse('marcarMentoria', args=[self.perfil.cpf]), {
        'mentor_cpf': self.perfil.cpf
    })
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['success'], f'Mentoria marcada com o mentor {self.perfil.nome}.')
