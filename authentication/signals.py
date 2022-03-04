from chats.models import HelpdeskChat


def create_user_helpdesk_chat(sender, instance, **kwargs):
    if not HelpdeskChat.objects.filter(user_id=instance.id):
        hd_chat = HelpdeskChat()
        hd_chat.user = instance
        hd_chat.save()
