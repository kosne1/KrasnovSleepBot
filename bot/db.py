from prisma import Client

async def init_user(message):
    db = Client()
    await db.connect()
    user = await db.user.find_unique(
        where={
            'chatId': message.from_user.id
        }
    )
    if user is None:
        await db.user.create(
            {
                'username': message.from_user.username,
                'chatId': message.from_user.id
            }
        )
    await db.disconnect()
    return user