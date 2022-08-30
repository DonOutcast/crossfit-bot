from loader import dp
from aiogram import types
from keyboards.default.system_kb import back_menu_keyboard
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
        await message.answer("Введите название тренировки:", reply_markup=back_menu_keyboard())
        await FSMAdminTeacherTraining.name_of_training.set()

    @staticmethod
    async def admin_answer_1(message: types.Message, state: FSMContext) -> None:
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['name_of_training'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherTraining.lvl_of_training.set()
        await message.answer("Выберите уровень сложности", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_2(message: types.Message, state: FSMContext) -> None:
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['lvl_of_training'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await state.finish()
        await FSMAdminTeacherComplex.name_of_complex.set()
        await message.answer("Введите название комплекса: ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_3(message: types.Message, state: FSMContext) -> None:
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['name_of_complex'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherComplex.repeat_complex.set()
        await message.answer("Введите количество кругов: ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_4(message: types.Message, state: FSMContext) -> None:
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['repeat_complex'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await state.finish()
        await FSMAdminTeacherExercises.name_of_exe.set()
        await message.answer("Введите название упражнения: ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_5(message: types.Message, state: FSMContext):
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['name_of_exe'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherExercises.reps.set()
        await message.answer("Введите количество подходов: ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_6(message: types.Message, state: FSMContext):
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['reps'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherExercises.again.set()
        await message.answer("Введите количество повторений: ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_7(message: types.Message, state: FSMContext):
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['again'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherExercises.temp_training.set()
        await message.answer("Введите темп(амрап, emom): ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_8(message: types.Message, state: FSMContext):
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['temp_training'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherExercises.type_training.set()
        await message.answer("Введите тип снаряда: ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_9(message: types.Message, state: FSMContext):
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['type_training'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherExercises.female.set()
        await message.answer("Введите норму для женщин: ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_10(message: types.Message, state: FSMContext):
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['female'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherExercises.male.set()
        await message.answer("Введите норму для мужчин: ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_11(message: types.Message, state: FSMContext):
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['male'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherExercises.relax_time.set()
        await message.answer("Введите время отдыха: ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_12(message: types.Message, state: FSMContext):
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['relax_time'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await FSMAdminTeacherExercises.work_time.set()
        await message.answer("Введите время работы: ", reply_markup=back_menu_keyboard())

    @staticmethod
    async def admin_answer_13(message: types.Message, state: FSMContext):
        logger.info(f"This is user message: {message.text} and type: {type(message.text)}")
        async with state.proxy() as data:
            data['work_time'] = message.text
        data = await state.get_data()
        state_logger.info(f"This is state data: {data} and type: {type(data)}")
        await state.finish()
        await message.answer("Тренеровка успешно добавлена: ", reply_markup=back_menu_keyboard())

    def register_handlers_admin(self):
        self.dp.register_message_handler(self.cmd_add_training, lambda message: "Добавить тренировку 🏹" in message.text, state=None)
        self.dp.register_message_handler(self.admin_answer_1, state=FSMAdminTeacherTraining.name_of_training)
        self.dp.register_message_handler(self.admin_answer_2, state=FSMAdminTeacherTraining.lvl_of_training)
        self.dp.register_message_handler(self.admin_answer_3, state=FSMAdminTeacherComplex.name_of_complex)
        self.dp.register_message_handler(self.admin_answer_4, state=FSMAdminTeacherComplex.repeat_complex)
        self.dp.register_message_handler(self.admin_answer_5, state=FSMAdminTeacherExercises.name_of_exe)
        self.dp.register_message_handler(self.admin_answer_6, state=FSMAdminTeacherExercises.reps)
        self.dp.register_message_handler(self.admin_answer_7, state=FSMAdminTeacherExercises.again)
        self.dp.register_message_handler(self.admin_answer_8, state=FSMAdminTeacherExercises.temp_training)
        self.dp.register_message_handler(self.admin_answer_9, state=FSMAdminTeacherExercises.type_training)
        self.dp.register_message_handler(self.admin_answer_10, state=FSMAdminTeacherExercises.female)
        self.dp.register_message_handler(self.admin_answer_11, state=FSMAdminTeacherExercises.male)
        self.dp.register_message_handler(self.admin_answer_12, state=FSMAdminTeacherExercises.relax_time)
        self.dp.register_message_handler(self.admin_answer_13, state=FSMAdminTeacherExercises.work_time)

a = AdminTeacher(dp)
a.register_handlers_admin()
