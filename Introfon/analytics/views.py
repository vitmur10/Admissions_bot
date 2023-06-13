from datetime import datetime

from asgiref.sync import sync_to_async

from .models import Analytics_actions, Analytics_User


def analytics(func: callable):
    total_messages = 0
    users = set()
    total_users = 0

    async def analytics_wrapper(message):
        """This wrapper function tracks and records analytics data before executing the original function."""
        nonlocal total_messages, total_users
        total_messages += 1
        if message.chat.id not in users and message.text == '/start':
            # If the user is new and sends the '/start' command, record them as a new user.
            users.add(message.chat.id)
            total_users += 1
            u = Analytics_User.objects.all()
            await sync_to_async(u.create)(
                quantity_user=total_users,
                data=datetime.now()
            )
        elif message.text != '/start':
            # If the message is not the '/start' command, record the action performed.
            a = Analytics_actions.objects.all()

            await sync_to_async(a.create)(
                clicks_quantity=total_messages,
                button_clicks=message.text,
                data=datetime.now()
            )

        return await func(message)

    return analytics_wrapper
