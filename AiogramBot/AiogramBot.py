import pika
import logging
from aiogram import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

available_states = ["Зарегистрироваться", "Отмена"]
name = config('name')
password = config('password')
host = config('host')
port = config('port')


class Registration(StatesGroup):
    waiting_registration = State()
    waiting_fio = State()
    waiting_respond = State()


async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_states:
        keyboard.add(name)
    await message.answer("Для продолжения стоит зарегистрироваться! Выберите нужную команду", reply_markup=keyboard)
    await Registration.waiting_registration.set()


async def fio_start(message: types.Message, state: FSMContext):
    if message.text not in available_states:
        await message.answer("Пожалуйста, выберите команду, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text.lower())

    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await Registration.next()
    await message.answer("Введите ФИО, н-р: Иванов иван иванович")


async def fio_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await Registration.next()
    await message.answer(f"Идёт проверка вашего ФИО")
    
    credentials = pika.PlainCredentials(name, password)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host, port, credentials=credentials))

    channel = connection.channel()

    channel.queue_declare(queue='registration')
    channel.basic_publish(exchange='',
                          routing_key='registration',
                          body=message.text)
    connection.close()
    
'''
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        
    channel.basic_consume(queue='registration',
                      auto_ack=True,
                      on_message_callback=callback)
    
    channel.start_consuming()
 '''

async def waiting_respond(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f"Молодец")
    await state.finish()


def register_handlers_food(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="reg", state="*")
    dp.register_message_handler(
        fio_start, state=Registration.waiting_registration)
    dp.register_message_handler(fio_chosen, state=Registration.waiting_fio)
    dp.register_message_handler(
        waiting_respond, state=Registration.waiting_respond)


async def main():

    # Настройка логирования в stdout
    logging.basicConfig(level=logging.INFO)

    # Объявление и инициализация объектов бота и диспетчера
    token = config('token', default='')
    bot = Bot(token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_food(dp)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == "__main__":
    # Запуск бота
    asyncio.run(main())
