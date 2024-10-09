from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from aiogram.types import ReplyKeyboardRemove


class fsm_registration(StatesGroup):
    fullname = State()
    age = State()
    phone_number = State()
    email = State()
    address = State()
    country = State()
    city = State()
    gender = State()
    photo = State()


async def start_fsm(message: types.Message):
    await message.answer(text='Введите фио:', reply_markup=buttons.cancel)
    await fsm_registration.fullname.set()


async def load_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await message.answer('Введите возраст:')
    await fsm_registration.next()


async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer('Введите номер телефона')
    await fsm_registration.next()


async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.answer('Введите почту:')
    await fsm_registration.next()


async def load_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await message.answer('Введите адрес проживание:')
    await fsm_registration.next()


async def load_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await message.answer('Введите страну где проживаете:')
    await fsm_registration.next()


async def load_country(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
    await message.answer('Введите город проживание:')
    await fsm_registration.next()


async def load_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await message.answer('Введите пол:')
    await fsm_registration.next()


async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await message.answer('Отправьте свою фотку:')
    await fsm_registration.next()


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

        await message.answer('Спасибо за регистрацию!')
        await message.answer_photo(photo=data['photo'],
                                   caption=f'Ваши данные:\n'
                                           f'ФИО - {data["fullname"]}\n'
                                           f'Возраст - {data["age"]}\n'
                                           f'Номер телефона - {data["phone_number"]}\n'
                                           f'Почта - {data["email"]}\n'
                                           f'Адрес - {data["address"]}\n'
                                           f'Страна - {data["country"]}\n'
                                           f'Город - {data["city"]}\n'
                                           f'Пол - {data["gender"]}\n')
        await state.finish()

async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено...', reply_markup=kb)

def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm,
                                Text(equals='Отмена', ignore_case=True),
                                state='*')

    dp.register_message_handler(start_fsm, commands=['reg'])
    dp.register_message_handler(load_fullname, state=fsm_registration.fullname)
    dp.register_message_handler(load_age, state=fsm_registration.age)
    dp.register_message_handler(load_phone_number, state=fsm_registration.phone_number)
    dp.register_message_handler(load_email, state=fsm_registration.email)
    dp.register_message_handler(load_address, state=fsm_registration.address)
    dp.register_message_handler(load_country, state=fsm_registration.country)
    dp.register_message_handler(load_city, state=fsm_registration.city)
    dp.register_message_handler(load_gender, state=fsm_registration.gender)
    dp.register_message_handler(load_photo, state=fsm_registration.photo,
                                content_types=['photo'])
