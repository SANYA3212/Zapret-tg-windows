# 🚀 TG Windows Proxy by SANYA

Локальный SOCKS5 прокси для подключения Telegram через WebSocket.  
Проект упаковывается в удобный `.exe` и не требует Python у конечного пользователя.

---

## 📁 Структура проекта

```
tg-ws-proxy-android/
│
├── src/
│   └── tg_sanya_proxy/
│       ├── app.py
│       ├── __main__.py
│       └── proxy_backend/
│           ├── tg_ws_proxy.py
│           └── tg_ws_proxy_NEW.py
│
├── build.bat
├── requirements.txt
├── pyproject.toml
├── TG_WINDOWS_Proxy_by_SANYA.spec
├── ЗАПУСК_SANYA.bat
└── README.md
```

---

# ⚙️ Сборка в EXE

## 🔧 Установка зависимостей

```
pip install -r requirements.txt
```

## 🧱 Сборка

Просто запусти:

```
build.bat
```

Или вручную:

```
pyinstaller TG_WINDOWS_Proxy_by_SANYA.spec
```

Файл появится в папке `dist/`

---

# ▶️ Использование EXE

## 📦 Подготовка

- Распакуй архив полностью
- НЕ запускай из ZIP
- Путь без русских букв (пример: C:\SanyaProxy)

## 🚀 Запуск

Запусти:

```
TG_WINDOWS_Proxy_by_SANYA.exe
```

---

## 🔌 Работа

1. Хост: `127.0.0.1`  
2. Порт: `1080`  

Нажми:
```
Запустить прокси
```

Статус должен стать **Активен**

Затем:
```
Подключить Telegram
```

---

## 📱 Ручная настройка Telegram

```
Тип: SOCKS5
Хост: 127.0.0.1
Порт: 1080
Логин: пусто
Пароль: пусто
```

---

# ⚠️ Проблемы

**Module not found** → не распаковал архив  
**Не запускается** → запуск от администратора  
**Антивирус блокирует** → добавить в исключения  

---

# 👤 Автор

SANYA
