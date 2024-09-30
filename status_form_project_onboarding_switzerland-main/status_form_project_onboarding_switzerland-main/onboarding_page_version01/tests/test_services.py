import unittest
from unittest.mock import patch
from app.services import get_card_titles_from_pipe, get_forms_status_for_card

class ServicesTestCase(unittest.TestCase):
    
    @patch('app.services.requests.post')
    def test_get_card_titles_from_pipe(self, mock_post):
        # Mock da resposta de requests.post
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'data': {
                'pipe': {
                    'phases': [
                        {
                            'cards': {
                                'edges': [
                                    {'node': {'title': 'Card 1'}},
                                    {'node': {'title': 'Card 2'}}
                                ]
                            }
                        }
                    ]
                }
            }
        }

        titles = get_card_titles_from_pipe(123456)
        self.assertEqual(titles, ['Card 1', 'Card 2'])

    # Adicione mais testes para outras funções de serviço aqui

if __name__ == '__main__':
    unittest.main()
