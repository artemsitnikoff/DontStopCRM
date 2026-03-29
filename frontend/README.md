# DontStopCRM Frontend

Vue 3 + TypeScript + Vite фронтенд для DontStopCRM.

## Быстрый старт

```bash
# Установка зависимостей
npm install

# Запуск в режиме разработки
npm run dev

# Сборка для продакшна
npm run build

# Предпросмотр билда
npm run preview
```

## Технологии

- **Vue 3** с Composition API
- **TypeScript** для типизации
- **Vite** как сборщик
- **Vue Router** для роутинга
- **Pinia** для state management
- **Tailwind CSS** для стилизации
- **Axios** для HTTP запросов

## Структура проекта

```
src/
├── api/              # HTTP клиент и API эндпоинты
├── components/       # Переиспользуемые компоненты
│   ├── ui/           # Базовые UI компоненты
│   ├── layout/       # Компоненты макета
│   └── domain/       # Бизнес-компоненты
├── composables/      # Vue композаблы
├── stores/           # Pinia хранилища
├── types/            # TypeScript типы
├── views/            # Страницы приложения
├── router/           # Настройка роутинга
└── utils/            # Утилиты и хелперы
```

## Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Настройте `VITE_API_URL` для подключения к бэкенду.

## Конвенции Digital Clouds

Проект следует строгим конвенциям Digital Clouds для Vue 3:

- ✅ Только `<script setup lang="ts">`
- ✅ Типизация с `defineProps<{}>()` и `defineEmits<{}>()`
- ✅ `ref()` для примитивов, `reactive()` для объектов
- ✅ API вызовы только через слой `api/`
- ✅ PascalCase для компонентов
- ✅ Никаких `any` типов

## Развертывание

```bash
npm run build
```

Результат сборки будет в папке `dist/`.