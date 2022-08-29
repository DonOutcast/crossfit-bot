from loader import dp
import logging
from aiogram import types
from states.all_states import FSMAdminTeacherTraining, FSMAdminTeacherComplex, FSMAdminTeacherExercises
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext


class AdminTeacher:
    def __init__(self, dp):
        self.dp = dp

    # @staticmethod
    # async def cmd_add_trainig(message: types.Message, state: FSMContext):
    #     await message.answer("Введите название тренировки:")

    @staticmethod
    async def cmd_add_training(message: types.Message, state: FSMContext):
        await message.answer("Введите название тренировки:")
        await FSMAdminTeacherTraining.name_of_training
        async with state.proxy() as data:
            data['name_of_training'] = message.text



    def register_handlers_admin(self):
        self.dp.register_message_handler(self.cmd_add_training, lambda message: "Добавить тренировку 🏹" in message.text, state=None)


