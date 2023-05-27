from aiogram.filters.callback_data import CallbackData


class TypeBeginnerCallBackData(CallbackData, prefix="type_beginner_"):
    pass


class TypeProceedingCallBackData(CallbackData, prefix="type_proceeding_"):
    pass


class TypeProfessionalBackData(CallbackData, prefix="type_professional_"):
    pass
