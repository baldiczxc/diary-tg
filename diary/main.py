import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiosqlite

router = Router()

# Состояния FSM
class DiaryStates(StatesGroup):
    AWAITING_SUBJECT_NAME = State()
    AWAITING_GRADE = State()

# Инициализация базы данных
async def init_db():
    async with aiosqlite.connect('diary.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject_name TEXT UNIQUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject_id INTEGER,
                grade INTEGER CHECK(grade BETWEEN 1 AND 5),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                day_of_week TEXT CHECK(day_of_week IN ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')),
                subject_name TEXT,
                time TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

        # Проверка наличия статических данных
        cursor = await db.execute('SELECT COUNT(*) FROM subjects WHERE user_id = 0')
        subjects_count = await cursor.fetchone()
        if subjects_count[0] == 0:
            # Добавление предметов из расписания
            subjects = [
                'География', 'Физика', 'Физическая культура',
                'Геометрия', 'История', 'Информатика', 'Русский язык', 'Биология',
                'Иностранный (англ.)', 'Литература', 'Химия', 'Алгебра и начала анализа',
                'Обществознание', 'Основы безопасности жизнедеятельности', 'Вероятность и статистика'
            ]
            for subject in subjects:
                await db.execute('''
                    INSERT OR IGNORE INTO subjects (user_id, subject_name)
                    VALUES (?, ?)
                ''', (0, subject))  # user_id = 0 для статических предметов
            await db.commit()

        cursor = await db.execute('SELECT COUNT(*) FROM schedule WHERE user_id = 0')
        schedule_count = await cursor.fetchone()
        if schedule_count[0] == 0:
            # Обновленное расписание звонков
            static_schedule = [
                # Понедельник - Пятница
                ('Понедельник', '08:20-09:00', 'Разговор о важном'),
                ('Понедельник', '09:10-09:50', 'География'),
                ('Понедельник', '10:00-10:40', 'Физика'),
                ('Понедельник', '11:00-11:40', 'Физика'),
                ('Понедельник', '12:00-12:40', 'Физическая культура'),
                ('Понедельник', '12:50-13:30', 'Геометрия'),
                ('Понедельник', '13:40-14:20', 'История'),
                ('Понедельник', '14:30-15:10', 'Информатика'),
                # Вторник
                ('Вторник', '08:20-09:00', 'Русский язык'),
                ('Вторник', '09:10-09:50', 'Русский язык'),
                ('Вторник', '10:00-10:40', 'Информатика'),
                ('Вторник', '11:00-11:40', 'Биология'),
                ('Вторник', '12:00-12:40', 'История'),
                ('Вторник', '12:50-13:30', 'Иностранный (англ.)'),
                ('Вторник', '13:40-14:20', 'Иностранный (англ.)'),
                # Среда
                ('Среда', '09:10-09:50', 'Физика'),
                ('Среда', '10:00-10:40', 'Литература'),
                ('Среда', '11:00-11:40', 'Литература'),
                ('Среда', '12:00-12:40', 'Химия'),
                ('Среда', '12:50-13:30', 'Алгебра и начала анализа'),
                ('Среда', '13:40-14:20', 'Алгебра и начала анализа'),
                # Четверг
                ('Четверг', '09:10-09:50', 'Физическая культура'),
                ('Четверг', '10:00-10:40', 'Физика'),
                ('Четверг', '11:00-11:40', 'Обществознание'),
                ('Четверг', '12:00-12:40', 'Алгебра и начала анализа'),
                ('Четверг', '12:50-13:30', 'Алгебра и начала анализа'),
                ('Четверг', '14:30-15:10', 'Россия - мои горизонты'),
                # Пятница
                ('Пятница', '09:10-09:50', 'Физическая культура'),
                ('Пятница', '10:00-10:40', 'Геометрия'),
                ('Пятница', '11:00-11:40', 'Физика'),
                ('Пятница', '12:00-12:40', 'Литература'),
                ('Пятница', '12:50-13:30', 'Геометрия'),
                ('Пятница', '13:40-14:20', 'Индивидуальный проект'),
                # Суббота (перемены по 10 минут)
                ('Суббота', '08:20-09:00', 'Обществознание'),
                ('Суббота', '09:10-09:50', 'Основы безопасности жизнедеятельности'),
                ('Суббота', '10:00-10:40', 'Информатика'),
                ('Суббота', '10:50-11:30', 'Информатика'),
                ('Суббота', '11:40-12:20', 'Вероятность и статистика'),
                ('Суббота', '12:30-13:10', 'Иностранный (англ.)'),
            ]
            for day, time, subject in static_schedule:
                await db.execute('''
                    INSERT OR IGNORE INTO schedule (user_id, day_of_week, time, subject_name)
                    VALUES (?, ?, ?, ?)
                ''', (0, day, time, subject))  # user_id = 0 для статического расписания
            await db.commit()

# Главное меню
async def main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🔢 Добавить оценку", callback_data="add_grade"),
        types.InlineKeyboardButton(text="🗑 Удалить оценку", callback_data="delete_grade")
    )
    builder.row(
        types.InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
        types.InlineKeyboardButton(text="🗓 Расписание", callback_data="schedule_menu")
    )
    return builder.as_markup()

# Меню расписания
async def schedule_menu_kb():
    builder = InlineKeyboardBuilder()
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    for day in days:
        builder.button(text=day, callback_data=f"schedule_{day}")
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(2)
    return builder.as_markup()

@router.message(F.text == '/start')
async def cmd_start(message: types.Message):
    await message.answer(
        "📖 Добро пожаловать в электронный дневник!\n"
        "Используйте кнопки ниже для управления:",
        reply_markup=await main_menu_kb()
    )

@router.callback_query(F.data == "main_menu")
async def return_main_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=await main_menu_kb()
    )

@router.callback_query(F.data == "schedule_menu")
async def schedule_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите день недели для просмотра расписания:",
        reply_markup=await schedule_menu_kb()
    )

# Добавление оценки
@router.callback_query(F.data == "add_grade")
async def start_add_grade(callback: types.CallbackQuery):
    async with aiosqlite.connect('diary.db') as db:
        cursor = await db.execute(
            'SELECT subject_id, subject_name FROM subjects WHERE user_id IN (?, 0)',  # Добавлено user_id = 0
            (callback.from_user.id,)
        )
        subjects = await cursor.fetchall()
    
    if not subjects:
        return await callback.answer("Сначала добавьте предметы!", show_alert=True)
    
    builder = InlineKeyboardBuilder()
    for subj_id, name in subjects:
        builder.button(text=name, callback_data=f"grade_subj_{subj_id}")
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(2)
    
    await callback.message.edit_text(
        "📝 Выберите предмет для оценки:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("grade_subj_"))
async def select_grade(callback: types.CallbackQuery, state: FSMContext):
    subject_id = callback.data.split("_")[-1]
    await state.update_data(current_subject=subject_id)
    
    builder = InlineKeyboardBuilder()
    for grade in range(1, 6):
        builder.button(text=str(grade), callback_data=f"set_grade_{grade}")
    builder.button(text="🔙 Назад", callback_data="add_grade")
    builder.adjust(5)
    
    await callback.message.edit_text(
        "🔢 Выберите оценку:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("set_grade_"))
async def save_grade(callback: types.CallbackQuery, state: FSMContext):
    grade = callback.data.split("_")[-1]
    data = await state.get_data()
    
    async with aiosqlite.connect('diary.db') as db:
        await db.execute(
            'INSERT INTO grades (user_id, subject_id, grade) VALUES (?, ?, ?)',
            (callback.from_user.id, data['current_subject'], grade)
        )
        await db.commit()
    
    await callback.answer(f"✅ Оценка {grade} добавлена!")
    await state.clear()
    await return_main_menu(callback)

# Удаление оценки
@router.callback_query(F.data == "delete_grade")
async def start_delete_grade(callback: types.CallbackQuery):
    async with aiosqlite.connect('diary.db') as db:
        cursor = await db.execute(
            'SELECT subject_id, subject_name FROM subjects WHERE user_id IN (?, 0)',  # Добавлено user_id = 0
            (callback.from_user.id,)
        )
        subjects = await cursor.fetchall()
    
    if not subjects:
        return await callback.answer("Сначала добавьте предметы!", show_alert=True)
    
    builder = InlineKeyboardBuilder()
    for subj_id, name in subjects:
        builder.button(text=name, callback_data=f"delete_grade_subj_{subj_id}")
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(2)
    
    await callback.message.edit_text(
        "🗑 Выберите предмет для удаления оценок:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("delete_grade_subj_"))
async def select_grade_to_delete(callback: types.CallbackQuery):
    subject_id = callback.data.split("_")[-1]
    async with aiosqlite.connect('diary.db') as db:
        cursor = await db.execute('''
            SELECT g.grade_id, g.grade, g.created_at
            FROM grades g
            WHERE g.user_id = ? AND g.subject_id = ?
            ORDER BY g.created_at DESC
        ''', (callback.from_user.id, subject_id))
        grades = await cursor.fetchall()
    
    if not grades:
        return await callback.answer("У вас нет оценок по этому предмету", show_alert=True)
    
    builder = InlineKeyboardBuilder()
    for grade_id, grade, created_at in grades:
        builder.button(
            text=f"Оценка: {grade} ({created_at[:10]})",
            callback_data=f"confirm_delete_grade_{grade_id}"
        )
    builder.button(text="🔙 Назад", callback_data="delete_grade")
    builder.adjust(1)
    
    await callback.message.edit_text(
        "Выберите оценку для удаления:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("confirm_delete_grade_"))
async def confirm_delete_grade(callback: types.CallbackQuery):
    grade_id = callback.data.split("_")[-1]
    async with aiosqlite.connect('diary.db') as db:
        await db.execute('DELETE FROM grades WHERE grade_id = ? AND user_id = ?', (grade_id, callback.from_user.id))
        await db.commit()
    
    await callback.answer("✅ Оценка успешно удалена!")
    await start_delete_grade(callback)

# Статистика
@router.callback_query(F.data == "stats")
async def show_stats(callback: types.CallbackQuery):
    async with aiosqlite.connect('diary.db') as db:
        cursor = await db.execute('''
            SELECT s.subject_name, 
                   AVG(g.grade), 
                   COUNT(g.grade),
                   MAX(g.created_at)
            FROM grades g
            JOIN subjects s ON g.subject_id = s.subject_id
            WHERE g.user_id = ?
            GROUP BY s.subject_name
        ''', (callback.from_user.id,))
        stats = await cursor.fetchall()
    
    if not stats:
        return await callback.answer("У вас пока нет оценок", show_alert=True)
    
    response = "📊 Ваша статистика:\n\n"
    for subject, avg, count, last_date in stats:
        response += (
            f"📚 {subject}:\n"
            f"▸ Средний балл: {avg:.2f}\n"
            f"▸ Всего оценок: {count}\n"
            f"▸ Последняя: {last_date[:10]}\n\n"
        )
    
    await callback.message.edit_text(
        response,
        reply_markup=InlineKeyboardBuilder().button(
            text="🔙 Назад", 
            callback_data="main_menu"
        ).as_markup()
    )

# Расписание
@router.callback_query(F.data.startswith("schedule_"))
async def show_day_schedule(callback: types.CallbackQuery):
    day = callback.data.split("_")[-1]
    async with aiosqlite.connect('diary.db') as db:
        cursor = await db.execute('''
            SELECT time, subject_name
            FROM schedule
            WHERE user_id = ? AND day_of_week = ?
            ORDER BY time
        ''', (0, day))  # user_id = 0 для статического расписания
        schedule = await cursor.fetchall()
    
    if not schedule:
        return await callback.answer(f"Расписание на {day} пусто", show_alert=True)
    
    response = f"🗓 Расписание на {day}:\n\n"
    for time, subject in schedule:
        response += f"⏰ {time} - {subject}\n"
    
    await callback.message.edit_text(
        response,
        reply_markup=InlineKeyboardBuilder()
        .button(text="🔙 Назад", callback_data="schedule_menu")
        .as_markup()
    )

async def main():
    await init_db()
    
    bot = Bot(token="TOKENBOT")
    dp = Dispatcher()
    dp.include_router(router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())