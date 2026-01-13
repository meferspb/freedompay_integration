# Быстрый старт: Установка FreedomPay Integration

## Проблема

Вы получаете ошибку:
```
App freedompay_integration not in apps.txt
```

## Решение (3 простых шага)

### Шаг 1: Добавьте приложение в apps.txt
```bash
echo "freedompay_integration" >> apps.txt
```

### Шаг 2: Установите приложение
```bash
bench --site erp.local install-app freedompay_integration
```

### Шаг 3: Настройте приложение
1. Перейдите в Frappe Desktop
2. Откройте "FreedomPay Settings"
3. Заполните обязательные поля

## Полные инструкции

### 1. Подключитесь к серверу
```bash
ssh user@your-server.com
```

### 2. Перейдите в bench директорию
```bash
cd /opt/frappe-server/frappe-bench
```

### 3. Добавьте приложение в apps.txt
```bash
echo "freedompay_integration" >> apps.txt
```

### 4. Установите приложение
```bash
bench --site erp.local install-app freedompay_integration
```

## Проверка

### Проверьте, что приложение добавлено в apps.txt
```bash
cat apps.txt
```

Вы должны увидеть `freedompay_integration` в списке.

### Проверьте, что приложение установлено
```bash
bench --site erp.local list-apps
```

Вы должны увидеть `freedompay_integration` в списке установленных приложений.

## Устранение неполадок

### Если вы все еще получаете ошибку:

1. **Проверьте текущую директорию**:
   ```bash
   pwd
   ```
   Убедитесь, что вы в `/opt/frappe-server/frappe-bench`

2. **Проверьте содержимое apps.txt**:
   ```bash
   cat apps.txt
   ```
   Убедитесь, что `freedompay_integration` есть в списке

3. **Проверьте права доступа**:
   ```bash
   ls -la apps.txt
   ```
   Убедитесь, что у вас есть права на запись

4. **Попробуйте с sudo** (если нужно):
   ```bash
   sudo echo "freedompay_integration" >> apps.txt
   ```

## Важно

- **Порядок важен**: Сначала добавьте в apps.txt, затем устанавливайте
- **Права доступа**: Убедитесь, что у вас есть права на запись в apps.txt
- **Директория**: Убедитесь, что вы в правильной bench директории

## Быстрые команды

Копируйте и вставляйте эти команды по одной:

```bash
cd /opt/frappe-server/frappe-bench
```

```bash
echo "freedompay_integration" >> apps.txt
```

```bash
bench --site erp.local install-app freedompay_integration
```

Это все, что нужно для установки FreedomPay Integration!
