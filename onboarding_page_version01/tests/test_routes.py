import unittest
from app import create_app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        # config da aplicação para testes
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()


    def test_index_route(self):
        response = self.client.get('/')
        self.assertIn(b'<title>Home</title>', response.data)  # atualizar aqui se mudar no html

    def test_status_route(self):
        response = self.client.get('/status')
        self.assertIn(b'<title>Project Onboarding Switzerland</title>', response.data)  # atualizar aqui se mudar no html

    
if __name__ == '__main__':
    unittest.main()
