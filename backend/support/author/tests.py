from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from author.models import Book, Ticket

User = get_user_model()


class AuthorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='author', password='secret123')
        self.other_user = User.objects.create_user(username='other-author', password='secret123')

        self.book = Book.objects.create(
            author=self.user,
            title='The First Book',
            isbn='1234567890123',
            genre='fi',
            mrp=200,
        )
        self.other_book = Book.objects.create(
            author=self.other_user,
            title='Another Book',
            isbn='9876543210987',
            genre='ro',
            mrp=300,
        )

        self.owned_ticket = Ticket.objects.create(
            query='Issue with my book',
            book=self.book,
            user=self.user,
            response='We are checking it',
        )
        self.other_ticket = Ticket.objects.create(
            query='Issue with another book',
            book=self.other_book,
            user=self.other_user,
            response='We resolved it',
        )

        self.client.force_authenticate(user=self.user)

    def test_books_list_returns_only_current_author_books(self):
        response = self.client.get('/books')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book.title)
        self.assertEqual(response.data[0]['isbn'], self.book.isbn)

    def test_tickets_list_returns_only_related_tickets(self):
        response = self.client.get('/tickets')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['query'], self.owned_ticket.query)
        self.assertEqual(response.data[0]['book'], self.book.title)

    @patch('author.views.Graph.build_graph')
    def test_create_ticket_returns_201_and_creates_ticket(self, mock_build_graph):
        mock_graph = Mock()
        mock_graph.invoke.return_value = {
            'messages': [Mock(content='Helpful response from assistant')]
        }
        mock_build_graph.return_value = mock_graph

        response = self.client.post('/create-ticket', {
            'query': 'How do I fix my sales report?',
            'isbn': self.book.isbn,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['query'], 'How do I fix my sales report?')
        self.assertEqual(response.data['response'], 'Helpful response from assistant')
        self.assertTrue(Ticket.objects.filter(query='How do I fix my sales report?', book=self.book).exists())

    def test_create_ticket_with_invalid_isbn_returns_400(self):
        response = self.client.post('/create-ticket', {
            'query': 'I need help with a missing book',
            'isbn': '0000000000000',
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid ISBN', response.data['isbn'][0])

    @patch('author.views.Graph.build_graph')
    def test_author_chat_returns_assistant_response(self, mock_build_graph):
        mock_graph = Mock()
        mock_graph.invoke.return_value = {
            'messages': [Mock(content='Here is the answer')]
        }
        mock_build_graph.return_value = mock_graph

        response = self.client.post('/author-chat', {'query': 'Summarize my latest sales'}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Here is the answer')
