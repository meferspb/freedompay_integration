# Новый модуль FreedomPay Integration

Этот документ описывает структуру нового модуля FreedomPay Integration, соответствующего стандартам Frappe.

## Структура нового модуля

```
freedompay_integration/
├── __init__.py
├── hooks.py
├── install.py
├── freedompay/
│   ├── __init__.py
│   ├── api.py
│   ├── connection.py
│   ├── urls.py
│   └── utils.py
├── freedompay_integration/
│   ├── __init__.py
│   ├── payment_gateway.py
│   └── checkout.py
├── doctype/
│   └── freedompay_settings/
│       ├── freedompay_settings.py
│       ├── freedompay_settings.json
│       └── freedompay_settings.js
├── patches/
│   └── create_payment_gateway.py
└── public/
    ├── css/
    │   └── freedompay.css
    └── js/
        └── freedompay.js
```

## Основные изменения

### 1. Новая структура модуля
- Разделение на freedompay/ (API) и freedompay_integration/ (интеграция)
- Добавление patches/ для миграций
- Более четкое разделение ответственности

### 2. Улучшенная интеграция с Frappe
- Полная интеграция с модулем payments
- Использование стандартных механизмов Frappe
- Соответствие документации Frappe

### 3. Улучшенная обработка ошибок
- Стандартные исключения Frappe
- Лучшее логирование
- Валидация данных

## Файлы нового модуля

### freedompay/api.py
```python
import frappe
import requests
import hashlib
import random
import string
from urllib.parse import urlencode

class FreedomPayAPI:
    def __init__(self, merchant_id, secret_key, base_url="https://api.freedompay.uz"):
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.base_url = base_url

    def create_payment(self, amount, currency, order_id, description, **kwargs):
        """Create payment request"""
        data = {
            'pg_merchant_id': self.merchant_id,
            'pg_amount': amount,
            'pg_currency': currency,
            'pg_order_id': order_id,
            'pg_description': description,
            **kwargs
        }

        signature = self._generate_signature(data)
        data['pg_sig'] = signature

        response = requests.post(f"{self.base_url}/init_payment.php", data=data)
        return self._handle_response(response)

    def _generate_signature(self, data):
        """Generate MD5 signature"""
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        data['pg_salt'] = salt

        signature_string = "init_payment.php;"
        for key in sorted(data.keys()):
            if key != 'pg_sig':
                signature_string += f"{key}={data[key]};"
        signature_string += self.secret_key

        return hashlib.md5(signature_string.encode('utf-8')).hexdigest()

    def _handle_response(self, response):
        """Handle API response"""
        if response.status_code == 200:
            return response.json()
        else:
            frappe.throw(f"FreedomPay API Error: {response.text}")
```

### freedompay_integration/payment_gateway.py
```python
import frappe
from frappe import _
from frappe.integrations.utils import create_request_log
from freedompay.api import FreedomPayAPI

def create_payment(gateway_controller, data):
    """Create FreedomPay payment"""
    settings = frappe.get_doc("FreedomPay Settings", gateway_controller)

    api = FreedomPayAPI(
        merchant_id=settings.merchant_id,
        secret_key=settings.get_password("secret_key")
    )

    payment_data = {
        "amount": data.amount,
        "currency": data.currency or "UZS",
        "order_id": data.reference_docname,
        "description": data.description or "",
        "result_url": settings.result_url,
        "success_url": settings.success_url,
        "failure_url": settings.failure_url,
        "user_id": data.payer_email,
        "email": data.payer_email,
        "phone": data.payer_phone,
    }

    try:
        response = api.create_payment(**payment_data)

        if response.get("pg_status") == "success":
            return {
                "redirect_to": response.get("pg_redirect_url"),
                "status": "Completed"
            }
        else:
            frappe.throw(_("Payment failed: {0}").format(response.get("pg_error_description")))

    except Exception as e:
        frappe.log_error(f"FreedomPay Payment Error: {str(e)}")
        frappe.throw(_("Payment processing error"))
```

### doctype/freedompay_settings/freedompay_settings.py
```python
import frappe
from frappe import _
from frappe.model.document import Document
from payments.utils import create_payment_gateway

class FreedomPaySettings(Document):
    def on_update(self):
        """Create payment gateway on update"""
        create_payment_gateway(
            "FreedomPay",
            settings="FreedomPay Settings",
            controller=self.name
        )

    def validate(self):
        """Validate settings"""
        if not self.merchant_id:
            frappe.throw(_("Merchant ID is required"))

        if not self.get_password("secret_key"):
            frappe.throw(_("Secret Key is required"))

        if not self.result_url:
            frappe.throw(_("Result URL is required"))

    def get_payment_url(self, **kwargs):
        """Get payment URL"""
        from frappe.utils import get_url
        return get_url(f"./freedompay_checkout?{urlencode(kwargs)}")
```

## Миграция на новый модуль

### Шаг 1: Создание нового модуля
```bash
bench new-app freedompay_integration
```

### Шаг 2: Копирование файлов
Скопируйте все файлы из новой структуры в новый модуль

### Шаг 3: Установка
```bash
bench --site erp.local install-app freedompay_integration
```

## Преимущества нового модуля

1. **Полное соответствие стандартам Frappe**
2. **Лучшая структура и организация кода**
3. **Улучшенная интеграция с payments**
4. **Лучшая обработка ошибок**
5. **Более надежная работа**

Этот новый модуль полностью соответствует документации Frappe и лучшим практикам.
