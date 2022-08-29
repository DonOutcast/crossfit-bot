from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdminTeacherTraining(StatesGroup):
    """This class for teacher filling in the table training """
    name_of_training = State()
    lvl_of_training = State()


class FSMAdminTeacherComplex(StatesGroup):
    """This class for teacher filling in the table complex"""
    name_of_complex = State()
    repeat_complex = State()


class FSMAdminTeacherExercises(StatesGroup):
    """This class for  filling in the teacher table """
    name_of_exe = State()
    reps = State()
    again = State()
    temp_training = State()
    type_training = State()
    female = State()
    male = State()
    relax_time = State()
    work_time = State()

