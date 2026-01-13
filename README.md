# FreedomPay Integration for Frappe

Этот модуль предоставляет интеграцию с платежной системой FreedomPay для платформы Frappe.

## Установка

1. Скопируйте папку `freedompay_integration` в ваш проект Frappe
2. Установите необходимые зависимости (requests, frappe)
3. Запустите миграцию для создания DocType настроек

## Настройка

1. Перейдите в **FreedomPay Settings** в Frappe
2. Заполните следующие поля:
   - **Merchant ID**: ID вашего магазина в FreedomPay
   - **Secret Key (для приема платежей)**: Секретный ключ для приема платежей
   - **Secret Key (для выплат)**: Секретный ключ для выплат (опционально)
   - **Base URL**: https://api.freedompay.uz (по умолчанию)
   - **Result URL**: URL для уведомления о результате оплаты
   - **Post Link**: URL для уведомления о результате выплаты
   - **Check URL**: URL для предварительной проверки платежа
   - **Success URL**: URL для перенаправления после успешной оплаты
   - **Failure URL**: URL для перенаправления после неудачной оплаты

## Использование

### Создание платежа

```python
from freedompay_integration.freedompay_integration import create_freedompay_payment

result = create_freedompay_payment("freedompay", {
    "amount": 100.00,
    "currency": "UZS",
    "description": "Оплата заказа",
    "reference_docname": "order-123",
    "payer_email": "customer@example.com",
    "success_url": "https://yourapp.com/success",
    "failure_url": "https://yourapp.com/failure"
})

if result["status"] == "Completed":
    redirect_url = result["redirect_to"]
    # Перенаправить пользователя на redirect_url
```

### Проверка статуса платежа

```python
from freedompay_integration.freedompay_integration import verify_freedompay_payment

status = verify_freedompay_payment("payment_id_123")
if status:
    print(f"Payment status: {status.get('pg_status')}")
```

### Создание выплаты

```python
from freedompay_integration.freedompay_integration import create_freedompay_payout

payout = create_freedompay_payout({
    "amount": 50.00,
    "currency": "UZS",
    "card_number": "4400440044004440",
    "cardholder_name": "JOHN DOE"
})
```

## API Documentation

Подробная документация FreedomPay доступна на:
https://freedompay.uz/docs/merchant-api/intro

## Тестирование

Запустите тесты:

```bash
python -m unittest freedompay_integration.test_freedompay
```

## Структура модуля

- `freedompay_api.py` - Основной API клиент
- `connection.py` - Обработка HTTP запросов и формирование подписей
- `urls.py` - Управление URL эндпоинтов
- `freedompay_integration.py` - Интеграция с Frappe
- `doctype/freedompay_settings/` - Настройки модуля

## Безопасность

- Все запросы подписываются с использованием MD5 подписи
- Секретные ключи хранятся в защищенном виде
- Поддерживается отдельный ключ для выплат

## Поддержка

Для вопросов по интеграции обращайтесь в техническую поддержку FreedomPay.
