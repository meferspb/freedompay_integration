# Как добавить freedompay_integration в apps.txt

## Быстрое решение

Выполните эту команду в вашей bench директории:

```bash
cd /opt/frappe-server/frappe-bench
echo "freedompay_integration" >> apps.txt
bench --site erp.local install-app freedompay_integration
```

## Пошаговая инструкция

### Шаг 1: Перейдите в bench директорию
```bash
cd /opt/frappe-server/frappe-bench
```

### Шаг 2: Проверьте текущее содержимое apps.txt
```bash
cat apps.txt
```

Вы должны увидеть что-то вроде:
```
frappe
erpnext
hrms
payments
crm
```

### Шаг 3: Добавьте freedompay_integration в apps.txt
```bash
echo "freedompay_integration" >> apps.txt
```

### Шаг 4: Проверьте, что приложение добавлено
```bash
cat apps.txt
```

Теперь вы должны увидеть freedompay_integration в конце списка.

### Шаг 5: Установите приложение
```bash
bench --site erp.local install-app freedompay_integration
```

### Шаг 6: Перезапустите bench (если нужно)
```bash
bench restart
```

## Альтернативный метод: Использование текстового редактора

Если вы предпочитаете использовать текстовый редактор:

```bash
cd /opt/frappe-server/frappe-bench
nano apps.txt
```

Добавьте строку `freedompay_integration` в конец файла, затем сохраните (Ctrl+O, Enter) и выйдите (Ctrl+X).

## Устранение неполадок

Если вы все еще получаете ошибку:

1. Убедитесь, что вы находитесь в правильной bench директории
2. Проверьте, что файл apps.txt существует и доступен для записи
3. Убедитесь, что freedompay_integration действительно находится в директории apps/
4. Проверьте права доступа: `ls -la apps.txt`

## Важно

После добавления в apps.txt и установки, приложение будет автоматически устанавливаться при создании новых сайтов или обновлении bench.
