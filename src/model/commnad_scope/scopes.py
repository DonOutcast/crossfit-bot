from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


class SetCommands:

    def __init__(self, bot: Bot):
        self.bot = bot
        self.commands = None

    async def _default_commands(self):
        """Set of commands with description"""
        await self.bot.set_my_commands([
            BotCommand(command="start", description="Старт"),
            BotCommand(command="help", description="Помощь"),
        ], scope=BotCommandScopeDefault())

    async def set_default_commands(self):
        commands = await self.bot.get_my_commands()
        if commands:
            await self.bot.delete_my_commands()
        await self._default_commands()