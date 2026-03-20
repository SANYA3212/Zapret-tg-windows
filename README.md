# TG_WINDOWS_Proxy_by_SANYA

Telegram WS Proxy для Windows с современным темным интерфейсом.

## Запуск

```bash
# Автоматически
ЗАПУСК_SANYA.bat

# Вручную
cd src
python -m tg_sanya_proxy
```

## Настройка Telegram

1. Telegram Desktop → Настройки → Продвинутые → Тип соединения
2. Использовать прокси → SOCKS5
3. Сервер: `127.0.0.1`, Порт: `1080`
4. Без авторизации

## Требования

- Python 3.8+
- `pip install -r requirements.txt`
