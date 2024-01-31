from django.db import models

from django.db import models

from users.models import User

class Room(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client', verbose_name='Клиент')
    master = models.OneToOneField(User, on_delete=models.CASCADE, related_name='master', verbose_name='Мастер')
    
    def __str__(self):
        return f'{self.client.email} - {self.master.email}'
    
    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    message_text = models.TextField(verbose_name='Текст сообщения')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Комната - #{self.room.id} - {self.message_text}'
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'