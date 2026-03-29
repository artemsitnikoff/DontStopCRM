# DontStopCRM

CRM в стиле десктопного Telegram + Kommo. AI-администратор ногтевого салона: ведёт календарь, записывает брони, переносит, ведёт досье клиентов, ставит себе задачи на следующий контакт.

## Экраны (MVP)

- **Дашборд** — статистика (total leads, by status/source, conversion rate), Chart.js графики, ближайшие задачи
- **Лиды** — канбан 4 колонки (Новый → Контакт → Квалифицирован → Выигран), drag-n-drop через vuedraggable
- **Чаты** — мессенджер Telegram-style (список чатов + переписка), WebSocket real-time
- **Календарь** — FullCalendar (месяц/неделя/день), drag-n-drop, модалка создания/редактирования событий

## Стек

- **Backend:** FastAPI + PostgreSQL + SQLAlchemy (async) + Alembic
- **Frontend:** Vue 3 + TypeScript + Vite + Tailwind CSS + Pinia
- **Библиотеки:** vuedraggable v4 (канбан), @fullcalendar/vue3 v6 (календарь), chart.js + vue-chartjs (дашборд)

## Структура проекта

```
backend/
├── src/
│   ├── main.py                 # FastAPI app, CORS, роутеры, exception handlers
│   ├── core/
│   │   ├── config.py           # Settings(BaseSettings) из .env
│   │   ├── database.py         # Async engine + sessionmaker + get_db
│   │   ├── security.py         # JWT create/verify, password hash (passlib+bcrypt)
│   │   └── exceptions.py       # Глобальный exception handler
│   ├── common/
│   │   ├── models.py           # BaseModel (id, created_at, updated_at)
│   │   ├── schemas.py          # BaseSchema, BaseResponse, PaginatedResponse, Pagination
│   │   └── dependencies.py     # get_current_user, get_current_active_user, get_current_admin_user
│   ├── auth/                   # User model, JWT login, register (admin-only)
│   ├── leads/                  # Lead CRUD, status PATCH для канбана, фильтры + пагинация
│   ├── chats/                  # Message CRUD, WebSocket с ConnectionManager, chat previews
│   ├── calendar/               # Event CRUD, date range filter, status update
│   └── dashboard/              # SQL-агрегация: leads by status/source, upcoming tasks, conversion
├── alembic/                    # Миграции (001 leads, 002 messages, 003 events)
├── .env                        # Локальные переменные (не в git)
├── requirements.txt            # Зависимости без пинов
└── Dockerfile

frontend/
├── src/
│   ├── main.ts                 # Vue app + Pinia + Router + dev auto-login
│   ├── App.vue                 # AppLayout wrapper
│   ├── style.css               # CSS variables (DC brand colors), Tailwind
│   ├── api/                    # Axios client + модули (leads, chats, calendar, dashboard, auth)
│   ├── types/                  # TypeScript интерфейсы (common, lead, chat, calendar, dashboard, auth)
│   ├── constants/leads.ts      # STATUS_LABELS/COLORS, SOURCE_LABELS/COLORS
│   ├── composables/            # useLeads, useChat, useCalendar, useDashboard, useAuth, useApi
│   ├── stores/useAuthStore.ts  # Pinia auth store (token + user в localStorage)
│   ├── router/index.ts         # Vue Router с auth guard
│   ├── components/
│   │   ├── ui/                 # AppButton, AppInput, AppModal, AppBadge, AppAvatar
│   │   ├── layout/             # AppSidebar (Telegram-style), AppLayout
│   │   └── domain/             # LeadCard, KanbanColumn, ChatListItem, MessageBubble,
│   │                           # ChatInput, ChatContent, EventModal, EventForm,
│   │                           # StatCard, UpcomingTasksTable
│   └── views/                  # DashboardView, LeadsView, ChatsView, CalendarView
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json

docker-compose.yml              # postgres + redis + app (для Docker-деплоя)
.env                            # Секреты через ${VAR} (не в git)
```

## Конвенции

### Backend (Digital Clouds FastAPI)
- Каждый модуль: router.py (тонкий), service.py (бизнес-логика), schemas.py, models.py, constants.py, exceptions.py, dependencies.py
- Роутеры НЕ содержат бизнес-логику — только оркестрация
- Кастомные exceptions вместо голых HTTPException в сервисах
- async для I/O, sync для CPU
- response_model на каждом эндпоинте
- Type hints: `X | None` (не Optional)
- Logging: lazy % formatting (не f-strings)
- Все эндпоинты защищены auth (кроме /login)

### Frontend (Digital Clouds Vue 3)
- ВСЕГДА `<script setup lang="ts">`
- Нет `any` — полная типизация
- API через `api/` слой, НЕ из компонентов напрямую
- Props: `defineProps<{}>()` с `withDefaults()`
- Composables: `use*.ts` — переиспользуемая логика
- Компоненты < 200 строк

## Цвета (dclouds.ru)

```css
--color-primary: #1929bb       /* синий — сайдбар, кнопки, акцент */
--color-primary-dark: #080c38  /* тёмный — hover кнопок */
--color-accent: #1929bb        /* = primary (синий, НЕ красный) */
--color-accent-light: #d1d4f1  /* светло-голубой — hover, выделения */
--color-cyan: #01faff          /* бирюзовый — декоративный */
--color-bg: #f4f4fc            /* фон */
--color-success: #017d0d       /* зелёный */
--color-warning: #e6a23c       /* оранжевый */
--color-danger: #f56c6c        /* красный (только ошибки) */
```

## Запуск (локально без Docker)

```bash
# Backend
cd backend
python3.13 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Создать PostgreSQL БД: createdb dnstp, createuser dnstp
# Скопировать .env из .env.example, указать DATABASE_URL
uvicorn src.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev  # http://localhost:3000

# Admin: admin@dnstp.ru / admin123
```

## API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| POST | /api/v1/auth/login | Логин (JSON: email + password) |
| POST | /api/v1/auth/register | Регистрация (admin-only) |
| GET | /api/v1/leads/ | Список лидов с фильтрами и пагинацией |
| POST | /api/v1/leads/ | Создать лида |
| PATCH | /api/v1/leads/{id} | Обновить лида |
| PATCH | /api/v1/leads/{id}/status | Сменить статус (канбан drag) |
| DELETE | /api/v1/leads/{id} | Удалить лида |
| GET | /api/v1/chats/ | Список чатов (превью с последним сообщением) |
| GET | /api/v1/chats/{lead_id}/messages | История сообщений |
| POST | /api/v1/chats/{lead_id}/messages | Отправить сообщение |
| WS | /api/v1/chats/ws/{lead_id}?token= | WebSocket real-time |
| GET | /api/v1/calendar/ | События с фильтрами по датам |
| POST | /api/v1/calendar/ | Создать событие |
| PATCH | /api/v1/calendar/{id} | Обновить событие |
| PATCH | /api/v1/calendar/{id}/status | Сменить статус |
| DELETE | /api/v1/calendar/{id} | Удалить событие |
| GET | /api/v1/dashboard/stats | Статистика дашборда |
