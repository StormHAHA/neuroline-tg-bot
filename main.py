import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "7973940253:AAHm90XxjRD0rd3z4QDlEMwhfIStXzrXQyg"
OWNER_ID = 835935469  # ID владельца бота

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    parent_name = State()                   # Имя родителя
    kid_name = State()                      # Имя ребенка
    contact_number = State()                # Контактный номер
    age = State()                           # Возраст ребенка
    pregnancy = State()                     # Как протекала беременность? (токсикоз, стрессы, угрозы)
    birth_term = State()                    # Каким был срок родов? (доношенный, недоношенный, переношенный)
    birth_process = State()                 # Как прошли роды?
    birth_cry = State()                     # Была ли задержка крика после рождения?
    birth_weight = State()                  # Каков был вес/рост при рождении?
    head_hold = State()                     # Во сколько начал держать голову?
    motor_development = State()             # Когда сел, пополз, пошел?
    speech_development = State()            # Когда появились первые звуки, слова, фразы?
    feeding = State()                       # Были ли особенности вскармливания? (грудное/искусственное, были ли сложности)
    current_difficulties = State()          # Что вызывает наибольшие затруднения?
    reaction_to_tasks = State()             # Как ребенок реагирует на новые задачи?
    behavior_features = State()             # Какие есть особенности поведения?
    social_interaction = State()            # Как ребенок взаимодействует с окружающими?
    sensory_sensitivity = State()           # Как ребенок переносит тактильный, звуковой, зрительный контакт?
    diagnosis = State()                     # Какие заключения?
    treatment = State()                     # Есть ли назначенное лечение (медикаменты, процедуры, БАДы)?

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Здравствуйте!\nПожалуйста, постарайтесь ответить на вопросы максимально подробно 😊\n")
    await message.answer("📌Введите ваше имя и фамилию (имя фамилия мамы/папы):")
    await state.set_state(Form.parent_name)

@dp.message(Form.parent_name)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(parent_name=message.text)
    await message.answer("📌Введите имя и фамилию ребенка:")
    await state.set_state(Form.kid_name)

@dp.message(Form.kid_name)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(kid_name=message.text)
    await message.answer("📌Введите контактный номер телефона:")
    await state.set_state(Form.contact_number)

@dp.message(Form.contact_number)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(contact_number=message.text)
    await  message.answer("📌Введите возраст ребенка:")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("📌Как протекала беременность? (токсикоз, стрессы, угрозы, другое)")
    await state.set_state(Form.pregnancy)

@dp.message(Form.pregnancy)
async def process_pregnancy(message: Message, state: FSMContext):
    await state.update_data(pregnancy=message.text)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Доношенный", callback_data="birth_term_full"),
             InlineKeyboardButton(text="Недоношенный", callback_data="birth_term_preterm")],
            [InlineKeyboardButton(text="Переношенный", callback_data="birth_term_postterm")]
        ]
    )
    await message.answer("📌Каким был срок родов?", reply_markup=keyboard)
    await state.set_state(Form.birth_term)

@dp.callback_query(Form.birth_term)
async def process_birth_term(callback: types.CallbackQuery, state: FSMContext):
    birth_term = callback.data.replace("birth_term_", "")
    birth_term = birth_term.replace("full", "Доношенный")
    birth_term = birth_term.replace("preterm", "Недоношенный")
    birth_term = birth_term.replace("postterm", "Переношенный")

    await state.update_data(birth_term=birth_term)
    await callback.message.answer("📌Как прошли роды? (естественные, кесарево сечение, гипоксия, асфиксия, стремительные, затяжные и т.д.)")
    await state.set_state(Form.birth_process)
    await callback.answer()

@dp.message(Form.birth_process)
async def process_birth_process(message: Message, state: FSMContext):
    await state.update_data(birth_process=message.text)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data="birth_cry_yes"),
             InlineKeyboardButton(text="Нет", callback_data="birth_cry_no")],
            [InlineKeyboardButton(text="Нет четкого ответа", callback_data="birth_cry_uncertain")]
        ]
    )
    await message.answer("📌Была ли задержка крика после рождения?", reply_markup=keyboard)
    await state.set_state(Form.birth_cry)

@dp.callback_query(Form.birth_cry)
async def process_birth_cry(callback: types.callback_query, state: FSMContext):
    birth_cry = callback.data.replace("birth_cry_", "")
    birth_cry = birth_cry.replace("yes", "Да")
    birth_cry = birth_cry.replace("no", "Нет")
    birth_cry = birth_cry.replace("uncertain", "Нет четкого ответа")
    await state.update_data(birth_cry=birth_cry)
    await callback.message.answer("📌Каков был вес/рост при рождении?")
    await state.set_state(Form.birth_weight)
    await callback.answer()

@dp.message(Form.birth_weight)
async def process_birth_weight(message: Message, state: FSMContext):
    await state.update_data(birth_weight=message.text)
    await message.answer("📌Во сколько начал держать голову?")
    await state.set_state(Form.head_hold)


@dp.message(Form.head_hold)
async def process_motor_development(message: Message, state: FSMContext):
    await state.update_data(motor_development=message.text)
    await message.answer("📌Когда сел, пополз, пошел?")
    await state.set_state(Form.motor_development)

@dp.message(Form.motor_development)
async def process_speech_development(message: Message, state: FSMContext):
    await state.update_data(speech_development=message.text)
    await message.answer("📌Когда появились первые звуки, слова, фразы?")
    await state.set_state(Form.speech_development)

@dp.message(Form.speech_development)
async def process_speech_development(message: Message, state: FSMContext):
    await state.update_data(speech_development=message.text)
    await message.answer("📌Были ли особенности вскармливания? (грудное/искусственное, были ли сложности)")
    await state.set_state(Form.feeding)

@dp.message(Form.feeding)
async def process_feeding(message: Message, state: FSMContext):
    await state.update_data(feeding=message.text)
    await message.answer("📌Какие есть актуальные трудности у ребенка?\n🔹Речь и коммуникация\n🔹Внимание и усидчивость\n🔹Память и мышление\n🔹Эмоциональная регуляция\n🔹Сенсорная чувствительность\n🔹Моторика (крупная, мелкая, координация)\n🔹Поведение (агрессия, истерики, тревожность, замкнутость)")
    await state.set_state(Form.current_difficulties)

@dp.message(Form.current_difficulties)
async def process_reaction_to_tasks(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="С интересом", callback_data="reaction_interest"),
             InlineKeyboardButton(text="Избегает", callback_data="reaction_avoidance")],
            [InlineKeyboardButton(text="Быстро устает", callback_data="reaction_fatigue")]
        ]
    )
    await message.answer("📌Как ребенок реагирует на новые задачи?", reply_markup=keyboard)
    await state.set_state(Form.reaction_to_tasks)

@dp.callback_query(Form.reaction_to_tasks)
async def process_reaction_to_tasks(callback: types.callback_query, state: FSMContext):
    reaction_to_tasks = callback.data.replace("reaction_", "")
    reaction_to_tasks = reaction_to_tasks.replace("interest", "С интересом")
    reaction_to_tasks = reaction_to_tasks.replace("avoidance", "Избегает")
    reaction_to_tasks = reaction_to_tasks.replace("fatigue", "Быстро устает")
    await state.update_data(reaction_to_tasks=reaction_to_tasks)
    await callback.message.answer("📌Какие есть особенности поведения?\n🔹Гиперактивность / заторможенность\n🔹Сложности со сменой деятельности\n🔹Тревожность, страхи\n🔹Агрессия, самоповреждение\n🔹Стимминги (махание руками, раскачивание, повторяющиеся движения)")
    await state.set_state(Form.behavior_features)
    await callback.answer()

@dp.message(Form.behavior_features)
async def process_behavior_features(message: Message, state: FSMContext):
    await state.update_data(behavior_features=message.text)
    await message.answer("📌Как ребенок взаимодействует с окружающими?\n🔹Охотно идет на контакт, поддерживает диалог\n🔹Общается только со взрослыми, избегает детей\n🔹Предпочитает одиночные игры\n🔹Есть ли реакция на имя?")
    await state.set_state(Form.social_interaction)

@dp.message(Form.social_interaction)
async def process_social_interaction(message: Message, state: FSMContext):
    await state.update_data(social_interaction=message.text)
    await message.answer("📌Как ребенок переносит тактильный, звуковой, зрительный контакт?\n🔹Любит / избегает прикосновений\n🔹Чувствителен к громким звукам / не реагирует\n🔹Избегает / ищет зрительный контакт")
    await state.set_state(Form.sensory_sensitivity)

@dp.message(Form.sensory_sensitivity)
async def process_sensory_sensitivity(message: Message, state: FSMContext):
    await state.update_data(sensory_sensitivity=message.text)
    await message.answer("📌Какие есть диагнозы, заключения?")
    await state.set_state(Form.diagnosis)

@dp.message(Form.diagnosis)
async def process_diagnosis(message: Message, state: FSMContext):
    await state.update_data(diagnosis=message.text)
    await message.answer("📌Есть ли назначенное лечение (медикаменты, процедуры, БАДы)?")
    await state.set_state(Form.treatment)

questions = {
    "parent_name": "✅Имя родителя:",
    "kid_name": "✅Имя ребенка:",
    "contact_number": "✅Контактный номер телефона:",
    "age": "✅Возраст ребенка:",
    "pregnancy": "✅Как протекала беременность?",
    "birth_term": "✅Каким был срок родов?",
    "birth_process": "✅Как прошли роды?",
    "birth_cry": "✅Была ли задержка крика после рождения?",
    "birth_weight": "✅Каков был вес/рост при рождении?",
    "head_hold": "✅Во сколько начал держать голову?",
    "motor_development": "✅Когда сел, пополз, пошел?",
    "speech_development": "✅Когда появились первые звуки, слова, фразы?",
    "feeding": "✅Были ли особенности вскармливания?",
    "current_difficulties": "✅Что вызывает наибольшие затруднения?",
    "reaction_to_tasks": "✅Как ребенок реагирует на новые задачи?",
    "behavior_features": "✅Какие есть особенности поведения?",
    "social_interaction": "✅Как ребенок взаимодействует с окружающими?",
    "sensory_sensitivity": "✅Как ребенок переносит тактильный, звуковой, зрительный контакт?",
    "diagnosis": "✅Какие диагнозы?",
    "treatment": "✅Есть ли назначенное лечение?",
}

@dp.message(Form.treatment)
async def process_treatment(message: Message, state: FSMContext):
    user_data = await state.update_data(treatment=message.text)
    await state.clear()

    # Формируем текст анкеты в формате вопрос/ответ
    result_text = "\n".join([f"{questions[key]} {value}" for key, value in user_data.items()])

    await bot.send_message(OWNER_ID, f"📋 Новая анкета:\n\n{result_text}")
    await message.answer("Спасибо! Ваши ответы отправлены.😁")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
