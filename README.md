# Бекенд для бронирования авиабилетов (Python)

[![hexlet-check](https://github.com/Xequrt/test-program-please-ignore-3-middle-python-project-428/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Xequrt/test-program-please-ignore-3-middle-python-project-428/actions)

REST API сервиса бронирования авиабилетов с поиском рейсов, оформлением, просмотром и отменой брони. Данные хранятся в PostgreSQL, фронтенд предоставляется Hexlet в виде готового npm-пакета.

**🌐 Демо:** https://test-program-please-ignore-3-middle-2wad.onrender.com

Учебный проект Хекслета: https://ru.hexlet.io/programs/test-program-please-ignore-3-middle-python

## Возможности

- 📍 Справочник городов (7 городов России)
- ✈️ Поиск рейсов по маршруту, дате и количеству пассажиров
- 🎫 Оформление брони с автоматическим расчётом стоимости
- 🔍 Просмотр брони по коду и фамилии
- ❌ Отмена брони
- 🔒 Защита от перебора кодов (одинаковые ответы на неверный код/фамилию)

## Стек технологий

- **Backend:** Python 3.13, FastAPI
- **Database:** PostgreSQL (psycopg 3)
- **Frontend:** React (готовый пакет от Hexlet)
- **Server:** Uvicorn
- **Testing:** pytest
- **CI/CD:** GitHub Actions
- **Deploy:** Render
- **Package Manager:** uv

## Установка

### Требования

- Python 3.13+
- PostgreSQL 13+
- Node.js 18+ (для установки фронтенда)
- uv (менеджер зависимостей Python)

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Xequrt/test-program-please-ignore-3-middle-python-project-428.git
cd test-program-please-ignore-3-middle-python-project-428
```

2. Создайте файл `.env` с подключением к PostgreSQL:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/flight_booking
PORT=8080
```

3. Установите зависимости:
```bash
make install
```

4. Соберите фронтенд:
```bash
make build
```

5. Запустите приложение:
```bash
make start
```

Приложение будет доступно по адресу: http://localhost:8080

## Использование

### API Endpoints

**Health Check**
```bash
GET /api/health
```

**Справочник городов**
```bash
GET /api/cities
```

**Поиск рейсов**
```bash
GET /api/flights?origin=MOW&destination=LED&date=2026-12-20&passengers=2
```

**Получить рейс по ID**
```bash
GET /api/flights/{id}
```

**Создать бронь**
```bash
POST /api/bookings
Content-Type: application/json

{
  "flightId": "1",
  "contact": {
    "email": "user@example.com",
    "phone": "+79991234567"
  },
  "passengers": [
    {
      "firstName": "Иван",
      "lastName": "Петров",
      "dateOfBirth": "1990-05-20",
      "documentNumber": "4509 123456"
    }
  ]
}
```

**Просмотр брони**
```bash
GET /api/bookings/{code}?lastName=Петров
```

**Отменить бронь**
```bash
POST /api/bookings/{code}/cancel
Content-Type: application/json

{
  "lastName": "Петров"
}
```

### Тестирование

Запуск тестов:
```bash
make test
```

### Структура проекта

```
.
├── app/
│   ├── main.py           # FastAPI приложение и эндпоинты
│   ├── db.py             # Подключение к PostgreSQL
│   ├── sql.py            # SQL запросы
│   ├── serializers.py    # Сериализация данных для JSON
│   ├── init_db.py        # Создание схемы БД
│   ├── seed_data.py      # Заливка справочных данных
│   └── tests/            # Тесты
├── contract/
│   ├── main.tsp          # Описание API в TypeSpec
│   └── tspconfig.yaml    # Конфигурация TypeSpec
├── public/               # Статика фронтенда
├── Makefile              # Команды сборки и запуска
└── pyproject.toml        # Зависимости Python
```

### База данных

**Таблицы:**
- `cities` - справочник городов
- `aviacompany` - авиакомпании
- `flights` - рейсы (генерируются на 30 дней вперёд)
- `bookings` - бронирования
- `passengers` - пассажиры в бронированиях

**Особенности:**
- Рейсы привязаны к текущей дате (30 дней от сегодня)
- Коды бронирований генерируются из алфавита без похожих символов (0, O, 1, I исключены)
- Работа с часовыми поясами (Москва → UTC)

## Контракт API

API описан в TypeSpec (`contract/main.tsp`). Спецификация OpenAPI генерируется командой:
```bash
npx tsp compile contract
```

## CI/CD

GitHub Actions автоматически запускает тесты на каждый push. Конфигурация: `.github/workflows/hexlet-check.yml`

## Деплой

Приложение развёрнуто на Render: https://test-program-please-ignore-3-middle-42zq.onrender.com/

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
