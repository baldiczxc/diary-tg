# Electronic Diary

The Electronic Diary is a Telegram bot that allows users to manage their grades, view statistics, and check their class schedule.

## Features

- **Add Grades**: Select a subject and add a grade.
- **Delete Grades**: Select a subject, then delete a specific grade.
- **View Statistics**: Average grade, number of grades, and the date of the last grade for each subject.
- **View Schedule**: Class schedule for each day of the week.

## Installation

1. Clone the repository or copy the project files.
2. Ensure you have Python 3.11 or higher installed.
3. Install the required libraries:
   ```bash
   pip install aiogram aiosqlite asyncio
   ```

## Running

1. Ensure you have a Telegram bot token. Replace `TOKENBOT` in the code with your token.
2. Replace the schedule with your desired schedule:
   ```python
            static_schedule = [
                # Monday - Friday
                ('Monday', '08:20-09:00', 'Important Conversations'),
                ('Monday', '09:10-09:50', 'Geography'),
                ('Monday', '10:00-10:40', 'Physics'),
                ('Monday', '11:00-11:40', 'Physics'),
                ('Monday', '12:00-12:40', 'Physical Education'),
                ('Monday', '12:50-13:30', 'Geometry'),
                ('Monday', '13:40-14:20', 'History'),
                ('Monday', '14:30-15:10', 'Computer Science'),
                # Tuesday
                ('Tuesday', '08:20-09:00', 'Russian Language'),
                ('Tuesday', '09:10-09:50', 'Russian Language'),
                ('Tuesday', '10:00-10:40', 'Computer Science'),
                ('Tuesday', '11:00-11:40', 'Biology'),
                ('Tuesday', '12:00-12:40', 'History'),
                ('Tuesday', '12:50-13:30', 'Foreign Language (English)'),
                ('Tuesday', '13:40-14:20', 'Foreign Language (English)'),
                # Wednesday
                ('Wednesday', '09:10-09:50', 'Physics'),
                ('Wednesday', '10:00-10:40', 'Literature'),
                ('Wednesday', '11:00-11:40', 'Literature'),
                ('Wednesday', '12:00-12:40', 'Chemistry'),
                ('Wednesday', '12:50-13:30', 'Algebra and Analysis'),
                ('Wednesday', '13:40-14:20', 'Algebra and Analysis'),
                # Thursday
                ('Thursday', '09:10-09:50', 'Physical Education'),
                ('Thursday', '10:00-10:40', 'Physics'),
                ('Thursday', '11:00-11:40', 'Social Studies'),
                ('Thursday', '12:00-12:40', 'Algebra and Analysis'),
                ('Thursday', '12:50-13:30', 'Algebra and Analysis'),
                ('Thursday', '14:30-15:10', 'Russia - My Horizons'),
                # Friday
                ('Friday', '09:10-09:50', 'Physical Education'),
                ('Friday', '10:00-10:40', 'Geometry'),
                ('Friday', '11:00-11:40', 'Physics'),
                ('Friday', '12:00-12:40', 'Literature'),
                ('Friday', '12:50-13:30', 'Geometry'),
                ('Friday', '13:40-14:20', 'Individual Project'),
                # Saturday (10-minute breaks)
                ('Saturday', '08:20-09:00', 'Social Studies'),
                ('Saturday', '09:10-09:50', 'Life Safety Basics'),
                ('Saturday', '10:00-10:40', 'Computer Science'),
                ('Saturday', '10:50-11:30', 'Computer Science'),
                ('Saturday', '11:40-12:20', 'Probability and Statistics'),
                ('Saturday', '12:30-13:10', 'Foreign Language (English)'),
            ]
   ```
3. Replace the subjects for grading:
   ```python
            subjects = [
                'Geography', 'Physics', 'Physical Education',
                'Geometry', 'History', 'Computer Science', 'Russian Language', 'Biology',
                'Foreign Language (English)', 'Literature', 'Chemistry', 'Algebra and Analysis',
                'Social Studies', 'Life Safety Basics', 'Probability and Statistics'
            ] 
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

## Usage

- Send the `/start` command in Telegram to start using the bot.
- Use the buttons to add or delete grades, view statistics, and check the schedule.

## Database Structure

- **subjects**: Table with subjects.
- **grades**: Table with grades.
- **schedule**: Table with the schedule.

## Dependencies

- `aiogram` — for working with the Telegram API.
- `aiosqlite` — for working with SQLite.
- `asyncio` — for asynchronous task execution.

## License

The project is distributed under the MIT license.

---

# Электронный дневник

Электронный дневник — это Telegram-бот, который позволяет пользователям управлять своими оценками, просматривать статистику и расписание занятий.

## Функционал

- **Добавление оценок**: Выберите предмет и поставьте оценку.
- **Удаление оценок**: Выберите предмет, затем удалите конкретную оценку.
- **Просмотр статистики**: Средний балл, количество оценок и дата последней оценки по каждому предмету.
- **Просмотр расписания**: Расписание занятий на каждый день недели.

## Установка

1. Клонируйте репозиторий или скопируйте файлы проекта.
2. Убедитесь, что у вас установлен Python 3.11 или выше.
3. Скачайте библиотеки:
   ```bash
   pip install aiogram aiosqlite asyncio
   ```

## Запуск

1. Убедитесь, что у вас есть токен Telegram-бота. Замените `TOKENBOT` в коде на ваш токен.
2. Замените расписание на нужное:
   ```python
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
   ```
3. Замените предметы для оценивания:
   ```python
            subjects = [
                'География', 'Физика', 'Физическая культура',
                'Геометрия', 'История', 'Информатика', 'Русский язык', 'Биология',
                'Иностранный (англ.)', 'Литература', 'Химия', 'Алгебра и начала анализа',
                'Обществознание', 'Основы безопасности жизнедеятельности', 'Вероятность и статистика'
            ] 
   ```
4. Запустите бота:
   ```bash
   python main.py
   ```

## Использование

- Отправьте команду `/start` в Telegram, чтобы начать работу с ботом.
- Используйте кнопки для добавления, удаления оценок, просмотра статистики и расписания.

## Структура базы данных

- **subjects**: Таблица с предметами.
- **grades**: Таблица с оценками.
- **schedule**: Таблица с расписанием.

## Зависимости

- `aiogram` — для работы с Telegram API.
- `aiosqlite` — для работы с SQLite.
- `asyncio` — для асинхронного выполнения задач.

## Лицензия

Проект распространяется под лицензией MIT.
