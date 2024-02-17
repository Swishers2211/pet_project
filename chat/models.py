from django.db import models

from django.db import models

from users.models import User

class Room(models.Model):
    sender = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sender', verbose_name='Отправитель')
    receiver = models.OneToOneField(User, on_delete=models.CASCADE, related_name='receiver', verbose_name='Получатель')
    
    def __str__(self):
        return f'{self.sender.email} - {self.receiver.email}'

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender', verbose_name='Отправитель')
    message_text = models.TextField(verbose_name='Текст сообщения')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Комната - #{self.room.id} - {self.message_text}'
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
