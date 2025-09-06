# Saleor Price Manager - Quick Start Guide

🚀 **Быстрый запуск проекта в 2 шага:**

## 📦 Шаг 1: Развертывание (DEPLOY)

```bash
./DEPLOY
```

Эта команда выполнит:
- ✅ Создание Python виртуального окружения
- ✅ Установку всех зависимостей из requirements.txt
- ✅ Сборку Rust модуля для высокопроизводительных вычислений
- ✅ Настройку конфигурации (.env файл)
- ✅ Проверку доступности Redis
- ✅ Установку frontend зависимостей

## 🔥 Шаг 2: Запуск (BANG)

```bash
./BANG
```

Эта команда:
- ✅ Загружает переменные окружения из .env
- ✅ Активирует Python виртуальное окружение
- ✅ Проверяет все зависимости
- ✅ Запускает FastAPI сервер с автоперезагрузкой

---

## 📋 Что получится после запуска:

- **🌐 API Server**: http://localhost:8000
- **📚 Swagger UI**: http://localhost:8000/docs
- **📖 ReDoc**: http://localhost:8000/redoc
- **💚 Health Check**: http://localhost:8000/health

---

## 🛠️ Дополнительные команды:

### Пересборка только Rust модуля:
```bash
./BUILD
```

### Остановка приложения:
```
Ctrl+C в терминале где запущен ./BANG
```

---

## ⚙️ Настройка конфигурации:

После первого запуска `./DEPLOY` отредактируйте файл `.env`:

```env
# Основные URL
APP_URL=http://localhost:8000
APP_FRONTEND_URL=http://localhost:3000

# Saleor API интеграция
SALEOR_API_URL=https://your-instance.saleor.cloud/graphql/
SALEOR_APP_TOKEN=your_saleor_app_token_here

# Redis для кеширования
REDIS_URL=redis://localhost:6379/0

# CORS настройки
CORS_ORIGINS=["http://localhost:3000", "https://your-instance.saleor.cloud"]
```

---

## 🐳 Docker альтернатива:

```bash
# Запуск с Docker Compose
docker-compose up --build

# Остановка
docker-compose down
```

---

## 🔧 Требования системы:

- **Python**: 3.11+ 
- **Node.js**: 22.x или 24.7.0 (для frontend)
- **Rust**: latest (устанавливается автоматически)
- **Redis**: 7.0+ (опционально для локальной разработки)

---

## 🚨 Устранение проблем:

### Redis недоступен:
```bash
# Установка и запуск Redis
sudo apt install redis-server  # Ubuntu
brew install redis            # macOS

# Или через Docker
docker run -d -p 6379:6379 redis:7.0
```

### Rust модуль не собирается:
```bash
# Переустановка Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
./BUILD
```

### Ошибка "Both VIRTUAL_ENV and CONDA_PREFIX are set":
```bash
# Временно отключите conda
conda deactivate
# Или удалите CONDA_PREFIX
unset CONDA_PREFIX
# Затем запустите сборку
./BUILD
```

### Maturin не может найти виртуальное окружение:
```bash
# Убедитесь что виртуальное окружение создано
./DEPLOY
# Активируйте окружение и пересоберите
source env/bin/activate
./BUILD
deactivate
```

### Проблемы с зависимостями Python:
```bash
# Очистка и пересоздание окружения
rm -rf env
./DEPLOY
```

---

**💡 Совет**: Все скрипты предоставляют подробный вывод о выполняемых действиях и возможных проблемах.