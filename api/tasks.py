from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

# Enviar email quando alguém começa a seguir um usuário
@shared_task
def send_follow_notification(follower_id, following_id):
    follower = User.objects.get(id=follower_id)
    following = User.objects.get(id=following_id)
    subject = f'Você tem um novo seguidor!'
    message = f'{follower.username} começou a seguir você.'
    recipient_list = [following.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
