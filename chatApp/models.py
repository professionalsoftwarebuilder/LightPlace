from django.db import models
from django.contrib.auth import get_user_model
from core.models import Profile

User = get_user_model()



TYPE_CHAT = (
    ('D', 'Dialog'),
    ('G', 'Group'),
)


class Chat(models.Model):
    cht_Name = models.CharField('Naam van chat', max_length=85, default='chat', null=False, blank=False)
    Contacts = models.ManyToManyField(Profile, related_name='chats', related_query_name='chat')
    cht_Ctrl = models.TextField('Control field')
    cht_Gen = models.DateTimeField('moment van creatie', auto_now_add=True)
    cht_Notes = models.TextField('Notes and info')
    cht_Type = models.CharField('Type Chat',
                                choices=TYPE_CHAT, default='D', blank=True, null=True, max_length=1,
                                help_text='Groeps chat of dialoog'
                                )


class Message(models.Model):
    msg_Author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    msg_Content = models.TextField()
    msg_TimeStamp = models.DateTimeField(auto_now_add=True)
    msg_ChatGroup = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return self.msg_Author.username

    # Let op: er moet hier GEEN self parameter worden meegegeven
    # anders werkt websocket niet en geeft ook geen melding waarom deze niet werkt
    # komt dan niet verder dan tot wanneer deze functie wordt aangeroepen
    def last_10_messages(chatGroupNm):
        print('in last 10 msg: ' + chatGroupNm)
        chatGroup = Chat.objects.get(cht_Name=chatGroupNm)
        return Message.objects.filter(msg_ChatGroup=chatGroup).order_by('msg_TimeStamp')[:10]

