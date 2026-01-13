# Руководство по установке FreedomPay Integration на удаленных серверах

Этот документ описывает, как установить FreedomPay Integration на удаленных серверах без использования shell скриптов.

## Проблема

При установке приложения через `bench --site erp.local install-app freedompay_integration` вы получаете ошибку:
```
App freedompay_integration not in apps.txt
```

Это нормальное поведение Frappe - приложение должно быть добавлено в `apps.txt` перед установкой.

## Решение для удаленных серверов

### Метод 1: Использование bench get-app с автоматическим добавлением

```bash
# 1. Подключитесь к серверу по SSH
ssh user@your-server.com

# 2. Перейдите в bench директорию
cd /opt/frappe-server/frappe-bench

# 3. Клонируйте приложение (это автоматически добавит его в apps.txt)
bench get-app https://github.com/meferspb/freedompay_integration.git

# 4. Установите приложение
bench --site erp.local install-app freedompay_integration
```

### Метод 2: Ручное добавление в apps.txt

```bash
# 1. Подключитесь к серверу по SSH
ssh user@your-server.com

# 2. Перейдите в bench директорию
cd /opt/frappe-server/frappe-bench

# 3. Добавьте приложение в apps.txt
echo "freedompay_integration" >> apps.txt

# 4. Клонируйте приложение
bench get-app https://github.com/meferspb/freedompay_integration.git

# 5. Установите приложение
bench --site erp.local install-app freedompay_integration
```

### Метод 3: Использование текстового редактора (nano)

```bash
# 1. Подключитесь к серверу по SSH
ssh user@your-server.com

# 2. Перейдите в bench директорию
cd /opt/frappe-server/frappe-bench

# 3. Откройте apps.txt в nano
nano apps.txt

# 4. Добавьте строку "freedompay_integration" в конец файла
# 5. Сохраните (Ctrl+O, Enter) и выйдите (Ctrl+X)

# 6. Клонируйте и установите приложение
bench get-app https://github.com/meferspb/freedompay_integration.git
bench --site erp.local install-app freedompay_integration
```

## Полный процесс установки

### Шаг 1: Подготовка сервера

```bash
# Подключение к серверу
ssh user@your-server.com

# Переход в bench директорию
cd /opt/frappe-server/frappe-bench
```

### Шаг 2: Добавление в apps.txt

Выберите один из методов выше или используйте этот универсальный метод:

```bash
# Проверка текущего содержимого apps.txt
cat apps.txt

# Добавление freedompay_integration
echo "freedompay_integration" >> apps.txt

# Проверка, что добавлено
cat apps.txt
```

### Шаг 3: Установка приложения

```bash
# Клонирование приложения
bench get-app https://github.com/meferspb/freedompay_integration.git

# Установка приложения
bench --site erp.local install-app freedompay_integration
```

### Шаг 4: Настройка приложения

После установки:

1. Перейдите в Frappe Desktop
2. Откройте "FreedomPay Settings"
3. Настройте обязательные поля:
   - **Merchant ID**: Ваш идентификатор от FreedomPay
   - **Secret Key**: Секретный ключ от FreedomPay
   - **Result URL**: URL для обработки результатов платежей
   - **Success URL**: URL для редиректа после успешного платежа
   - **Failure URL**: URL для редиректа после неудачного платежа

### Шаг 5: Перезапуск bench (опционально)

```bash
bench restart
```

## Устранение неполадок

### Ошибка: "App freedompay_integration not in apps.txt"

**Решение**:
```bash
# Проверьте содержимое apps.txt
cat apps.txt

# Если freedompay_integration отсутствует, добавьте его
echo "freedompay_integration" >> apps.txt

# Попробуйте установить снова
bench --site erp.local install-app freedompay_integration
```

### Ошибка: "Module payments not installed"

**Решение**:
```bash
# Установите модуль payments
bench get-app https://github.com/frappe/payments.git
bench --site erp.local install-app payments

# Затем установите freedompay_integration
bench --site erp.local install-app freedompay_integration
```

### Ошибка: "Permission denied"

**Решение**:
```bash
# Проверьте права доступа
ls -la apps.txt

# Если нужно, измените права
chmod 644 apps.txt

# Или используйте sudo (если вы не root)
sudo echo "freedompay_integration" >> apps.txt
```

## Автоматизация для удаленных серверов

Если вы часто устанавливаете приложение на разных серверах, создайте текстовый файл с командами и копируйте его на сервер:

```bash
# Создайте файл install_commands.txt на локальной машине
cat > install_commands.txt << 'EOF'
cd /opt/frappe-server/frappe-bench
echo "freedompay_integration" >> apps.txt
bench get-app https://github.com/meferspb/freedompay_integration.git
bench --site erp.local install-app freedompay_integration
EOF

# Скопируйте на сервер
scp install_commands.txt user@your-server.com:/tmp/

# Подключитесь к серверу и выполните команды
ssh user@your-server.com
source /tmp/install_commands.txt
```

## Важные заметки

1. **Порядок важно**: Сначала добавьте в apps.txt, затем клонируйте, затем устанавливайте
2. **Права доступа**: Убедитесь, что у вас есть права на запись в apps.txt
3. **Зависимости**: Убедитесь, что модуль payments установлен
4. **Безопасность**: Используйте SSH ключи для безопасного подключения

Это руководство должно помочь вам установить FreedomPay Integration на любых удаленных серверах без необходимости использования IDE или shell скриптов.
