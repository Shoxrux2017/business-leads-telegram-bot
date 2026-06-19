# Business Leads Telegram Bot

Telegram-бот для приема заявок от клиентов.

Проект подходит для кафе, учебных центров, клиник, магазинов и сервисных компаний.

## Что умеет бот

* Принимает заявку через Telegram
* Спрашивает имя клиента
* Спрашивает номер телефона
* Позволяет выбрать услугу или товар
* Принимает комментарий
* Сохраняет заявку в SQLite
* Отправляет уведомление администратору в Telegram

## Стек

* Python
* aiogram
* SQLite
* python-dotenv
* Telegram Bot API

## Как работает

Клиент нажимает `/start`.

Бот задает вопросы:

1. Имя
2. Телефон
3. Услуга / товар
4. Комментарий

После этого администратор получает уведомление о новой заявке.

## Установка

Создать виртуальное окружение:

```powershell
python -m venv .venv
```

Активировать окружение:

```powershell
.venv\Scripts\activate
```

Установить зависимости:

```powershell
pip install -r requirements.txt
```

Создать файл `.env`:

```env
BOT_TOKEN=PASTE_YOUR_BOT_TOKEN_HERE
ADMIN_ID=YOUR_TELEGRAM_ID
DATABASE_PATH=leads.db
```

Запустить бота:

```powershell
python main.py
```

## Скриншоты

### Диалог клиента с ботом

![Client flow](screenshots/client-flow.png)

### Уведомление администратору

![Admin notification](screenshots/admin-notification.png)

## Важно

Файл `.env` нельзя публиковать в GitHub, потому что там находится токен Telegram-бота.

## Возможные доработки

* Google Sheets integration
* Laravel admin panel
* Flutter mobile app
* Email notifications
* CRM dashboard
* Export to Excel
