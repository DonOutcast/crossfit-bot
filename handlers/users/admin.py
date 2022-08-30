from loader import dp
import logging
from aiogram import types
from states.all_states import FSMAdminTeacherTraining, FSMAdminTeacherComplex, FSMAdminTeacherExercises
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from logs.loggers import logger_Don_info

logger = logger_Don_info("DonOutcast", "logs/test.log")
state_logger = logger_Don_info("Doni", "logs/state.log")


class AdminTeacher:

    def __init__(self, dp):
        self.dp = dp

    @staticmethod
    async def cmd_add_training(message: types.Message, state: FSMContext) -> None:
        await message.answer("Введите название тренировки:")
        await FSMAdminTeacherTraining.name_of_training.set()

    @staticmethod
    async def admin_answer_1(message: types.Message, state: FSMContext) -> None:
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['name_of_training'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherTraining.lvl_of_training.set()
        await message.answer("Выберите уровень сложности")

    @staticmethod
    async def admin_answer_2(message: types.Message, state: FSMContext) -> None:
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['lvl_of_training'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await state.finish()
        await FSMAdminTeacherComplex.name_of_complex.set()
        await message.answer("Введите название комплекса: ")

    @staticmethod
    async def admin_answer_3(message: types.Message, state: FSMContext) -> None:
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['name_of_complex'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherComplex.repeat_complex.set()
        await message.answer("Введите количество кругов: ")

    @staticmethod
    async def admin_answer_4(message: types.Message, state: FSMContext) -> None:
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['repeat_complex'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await state.finish()

        await message.answer("Введите количество кругов: ")


    def register_handlers_admin(self):
        self.dp.register_message_handler(self.cmd_add_training, lambda message: "Добавить тренировку 🏹" in message.text, state=None)
        self.dp.register_message_handler(self.admin_answer_1, state=FSMAdminTeacherTraining.name_of_training)
        self.dp.register_message_handler(self.admin_answer_2, state=FSMAdminTeacherTraining.lvl_of_training)
        self.dp.register_message_handler(self.admin_answer_3, state=FSMAdminTeacherComplex.name_of_complex)


a = AdminTeacher(dp)
a.register_handlers_admin()
