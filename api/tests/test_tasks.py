from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from api.tasks import send_follow_notification

class TestTasks(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@test.com')
        self.user2 = User.objects.create_user(username='user2', email='user2@test.com')

    def test_send_follow_notification(self):
        send_follow_notification(self.user1.id, self.user2.id)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.user1.username, mail.outbox[0].body)
