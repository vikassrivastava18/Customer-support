from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from author.models import Book, Ticket

User = get_user_model()


class StaffApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='staff_admin',
            email='staff@example.com',
            password='secret123',
        )
        self.author_user = User.objects.create_user(
            username='author_user',
            email='author@example.com',
            password='secret123',
        )

        self.book = Book.objects.create(
            author=self.author_user,
            title='Sample Book',
            isbn='1111111111111',
            genre='fi',
            mrp=250,
        )

        self.ticket = Ticket.objects.create(
            query='Issue with tax invoice',
            book=self.book,
            user=self.author_user,
            response='Waiting for review',
            status='pr',
        )
        self.second_ticket = Ticket.objects.create(
            query='Issue with shipping label',
            book=self.book,
            user=self.author_user,
            response='Looking into it',
            status='op',
        )

    def test_staff_can_list_all_tickets(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get('/staff/tickets')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual({item['query'] for item in response.data}, {
            'Issue with tax invoice',
            'Issue with shipping label',
        })

    def test_staff_can_update_ticket_status_and_response(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.patch(
            f'/staff/tickets/{self.ticket.id}',
            {'status': 're', 'response': 'Resolved after review'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 're')
        self.assertEqual(self.ticket.response, 'Resolved after review')

    def test_non_admin_cannot_access_staff_ticket_list(self):
        self.client.force_authenticate(user=self.author_user)

        response = self.client.get('/staff/tickets')

        self.assertEqual(response.status_code, 403)
