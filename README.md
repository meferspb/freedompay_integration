# FreedomPay Integration for Frappe/ERPNext

Этот модуль предоставляет интеграцию с платежной системой FreedomPay для платформы Frappe и ERPNext.

## Установка

### Метод 1: Установка через bench (рекомендуется)

```bash
# 1. Перейдите в bench директорию
cd /opt/frappe-server/frappe-bench

# 2. Добавьте приложение в apps.txt
echo "freedompay_integration" >> apps.txt

# 3. Клонируйте приложение
bench get-app https://github.com/meferspb/freedompay_integration.git

# 4. Установите приложение
bench --site erp.local install-app freedompay_integration
```

### Метод 2: Быстрая установка (если bench get-app автоматически добавляет в apps.txt)

```bash
cd /opt/frappe-server/frappe-bench
bench get-app https://github.com/meferspb/freedompay_integration.git
bench --site erp.local install-app freedompay_integration
```

### Метод 3: Для удаленных серверов

Смотрите полное руководство в [REMOTE_INSTALLATION_GUIDE.md](REMOTE_INSTALLATION_GUIDE.md)

## Требования

- Frappe Framework v14+
- ERPNext (опционально)
- Payments App (рекомендуется для полной интеграции)
- Python 3.8+
- Node.js 14+

## Зависимости

Приложение автоматически устанавливает следующие зависимости:
- `requests` - для HTTP запросов
- Модуль `payments` (если используется полная интеграция)

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

3. Сохраните настройки - это автоматически создаст Payment Gateway

## Автоматическая настройка

После установки приложение автоматически:
- Создает DocType "FreedomPay Settings"
- Создает запись настроек по умолчанию
- Создает Payment Gateway (если установлен модуль payments)
- Проверяет обязательные поля

## Устранение неполадок

### Ошибка: "App freedompay_integration not in apps.txt"

**Решение**: Добавьте приложение в apps.txt перед установкой:
```bash
echo "freedompay_integration" >> apps.txt
```

### Ошибка: "Module payments not installed"

**Решение**: Установите модуль payments:
```bash
bench get-app https://github.com/frappe/payments.git
bench --site erp.local install-app payments
```

### Ошибка: "Merchant ID is required"

**Решение**: Настройте Merchant ID в FreedomPay Settings

## Обновление

Для обновления приложения:
```bash
cd /opt/frappe-server/frappe-bench
bench update --pull freedompay_integration
bench --site erp.local migrate
```

## Удаление

Для удаления приложения:
```bash
bench --site erp.local uninstall-app freedompay_integration
bench remove-from-installed-apps freedompay_integration
```

## Документация

- [Полное руководство по установке](REMOTE_INSTALLATION_GUIDE.md)
- [Документация FreedomPay API](https://freedompay.uz/docs/merchant-api/intro)
- [Frappe Payments Integration](https://github.com/frappe/payments)

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
