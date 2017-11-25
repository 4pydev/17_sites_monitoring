# Скрипт для мониторинга сайтов

Программа проверяет состояние сайтов. 
На вход принимает путь к текстовому файл с URL адресами для проверки. 
На выходе - статус каждого сайта по результатам следующих проверок:

  * сервер отвечает на запрос статусом HTTP 200;
  * доменное имя сайта проплачено как минимум на 1 месяц вперед.

# Исползование и пример вывода

Для запуска необходим Python 3.5.

```bash
$ python3 check_sites_health.py <path-to-your-data-file>

https://github.com: OK
Expiry date check: OK
...
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
