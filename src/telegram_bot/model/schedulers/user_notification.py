from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def users_notification(bot: Bot):
    print("Просто зашел сюда потусить")
    await bot.send_message(chat_id=1134902789, text="Привет")


def register(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler.add_job(users_notification, trigger='interval', seconds=30, args=(bot,))
