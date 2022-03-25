import app.mongoDB as mongoDB
import app.rabbit as rabbit
import json
import pymongo
import logging
from decouple import config
from aiogram import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

unregister_user_keyboard = ["Зарегистрироваться", "Отмена"]
register_user_keyboard = ["Отменить регистрацию"]

class Registration(StatesGroup):
    waiting_registration = State()
    waiting_fio = State()
    waiting_respond = State()

async def cmd_start(message: types.Message):
    
    users_collection = mongoDB.init_collection('users')
    result = mongoDB.find_document(users_collection, {'_telegram_id': message.from_user.id})
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if result == None:
        for name in unregister_user_keyboard:
            keyboard.add(name)
        await message.answer("Для продолжения стоит зарегистрироваться! Выберите нужную команду", reply_markup=keyboard)
        await Registration.waiting_registration.set()
    else:
        for name in register_user_keyboard:
            keyboard.add(name)
        await message.answer(f"Привет, {result.get('fio')}", reply_markup = keyboard)

async def fio_start(message: types.Message, state: FSMContext):

    if message.text.lower() != 'зарегистрироваться':
        await message.answer("Пожалуйста, выберите команду, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text)

    await Registration.waiting_fio.set()
    await message.answer("Введите ФИО, н-р: Иванов Иван Иванович", reply_markup=types.ReplyKeyboardRemove())

async def fio_chosen(message: types.Message, state: FSMContext):
    
    users_collection = mongoDB.init_collection('users')
    result = mongoDB.find_document(users_collection, {'fio': message.text})
    if result == None:
        await message.answer(f'Пользователя {message.text} нет в базе данных! Обратитесь в отдел персонала')
    else:
        result['_telegram_id'] = message.from_user.id
        mongoDB.update_document(users_collection, {'_id': result.get('_id')}, result)
        del result['_id']
        rabbit.send('registration', 'registration', json.dumps(result)) # подумать, как пустить это отдельным потоком...
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in register_user_keyboard:
            keyboard.add(name)
        await message.answer(f"Добро пожаловать, {result.get('fio')}", reply_markup=keyboard)
    await state.finish()

async def fio_unregister(message: types.Message):
    
    users_collection = mongoDB.init_collection('users')
    result = mongoDB.find_document(users_collection, {'_telegram_id': message.from_user.id})
    if result == None:
        await message.answer(f'Пользователь не зарегистрирован в телеграм-боте!')
    else:
        result['_telegram_id'] = ''
        mongoDB.update_document(users_collection, {'_id': result.get('_id')}, result)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in unregister_user_keyboard:
            keyboard.add(name)
        await message.answer("Регистрация пользователя отменена!",reply_markup = keyboard)
    
def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_start, lambda msg: msg.text.lower() == 'отмена', state="*")
    dp.register_message_handler(fio_unregister, lambda msg: msg.text.lower() == 'отменить регистрацию', state="*")
    dp.register_message_handler(fio_start, lambda msg: msg.text.lower() == 'зарегистрироваться', state="*")
    dp.register_message_handler(fio_start, state=Registration.waiting_registration)
    dp.register_message_handler(fio_chosen, state=Registration.waiting_fio)

async def main():

    # Create the client
    client = pymongo.MongoClient('localhost', 27017)

    # Connect to our database
    db = client['TestBot']

    # Настройка логирования в stdout
    logging.basicConfig(level=logging.INFO)

    # Объявление и инициализация объектов бота и диспетчера
    token = config('token', default='')
    bot = Bot(token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_registration(dp)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

if __name__ == "__main__":
    # Запуск бота
    asyncio.run(main())
