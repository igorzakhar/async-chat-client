# CLI клиент для подключения к чату.

Задача: написать программу для подключения к чату через командную строку.
Функции программы:
1. Подключается к указанному чат серверу;
2. Сохраняет историю переписки;
3. Отправляет сообщения в чат.

## Как установить

Для запуска скриптов нужен предустановленный Python версии не ниже 3.7+.
Также в программе используются следующие сторонние библиотеки:
- aiofile [https://github.com/mosquito/aiofile](https://github.com/mosquito/aiofile);
- aioconsole [https://github.com/vxgmichel/aioconsole](https://github.com/vxgmichel/aioconsole).

Рекомендуется устанавливать зависимости в виртуальном окружении, используя [virtualenv](https://github.com/pypa/virtualenv), [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) или [venv](https://docs.python.org/3/library/venv.html).

1. Скопируйте репозиторий в текущий каталог. Воспользуйтесь командой:
```bash
$ git clone https://github.com/igorzakhar/async-chat-client.git async_chat_client
```
После этого программа будет скопирована в каталог ```async_chat_client```

2. Создайте и активируйте виртуальное окружение:
```bash
$ cd async_chat_client # Переходим в каталог с программой
$ python3 -m venv my_virtual_environment # Создаем виртуальное окружение
$ source my_virtual_environment/bin/activate # Активируем виртуальное окружение
```

3. Установите сторонние библиотеки  из файла зависимостей:
```bash
$ pip install -r requirements.txt # В качестве альтернативы используйте pip3
```

## Запуск скрипта для чтения чата (chat_client_reader.py).
```bash
$ python3 chat_client_reader.py
```
Аргументы командной строки:
```
usage: chat_client_reader.py [-h] [--host HOST] [--port PORT] [--history  HISTORY]
```
- ```-h, --help``` - Вызов справки.
- ```--host HOST ``` -  Адрес чат-сервера (значение по умолчанию ```minechat.dvmn.org```)
- ```--port PORT``` - TCP порт чат-сервера (значение по умолчанию ```5000```).
- ```--history  HISTORY``` -  Путь к файлу в котором сохраняется история переписки в чате(по умолчанию текущая директория, файл ```chat.history```).

## Запуск скрипта для отправки сообщений в чат (chat_client_reader.py).
Скрипт включает в себя регистрацию нового пользователя и авторизацию существующего пользователя.
##### 1. Пример запуска скрипта для регистрации нового пользователя:  
```bash
$ python3 chat_client_reader.py --username  YourUsername
```
Если имя не указано то генерируется чат-сервером и отправляется в ответном сообщении вместе с токеном. Отследить создание нового пользователя можно через режим отладки ```--debug```. Пример запуска:
```bash
$ python3 chat_client_reader.py --debug
DEBUG:root:Установлено соединение.
DEBUG:sender:Hello %username%! Enter your personal hash or leave it empty to create new account.
DEBUG:sender:Sent message: '\n'
DEBUG:sender:Enter preferred nickname below:
DEBUG:sender:Sent message: '\n'
DEBUG:sender:{"nickname": "New user", "account_hash": "..."}
```
##### 2. Пример запуска скрипта для аворизации и отправки сообщений:
```bash
$ python3 chat_client_reader.py --token xxx-xxxx.... --message YourMessage
```
Если не указан аргумент ```--message``` то запустится текстовый интерфейс c приглашением для ввода и отправки сообщений:
```bash
$ python3 chat_client_reader.py --token xxx-xxxx.... 
>>> Hello world!
>>> 
```

Аргументы командной строки:
```
usage: chat_client_writer.py [-h] [--host HOST] [--port PORT] [--token TOKEN]
                             [--debug] [--username USERNAME]
                             [--message MESSAGE]

```
- ```-h, --help``` - Вызов справки.
- ```--host HOST ``` -  Адрес чат-сервера (значение по умолчанию ```minechat.dvmn.org```)
- ```--port PORT``` - TCP порт чат-сервера (значение по умолчанию ```5050```).
- ```--token TOKEN``` - Токен зарегистрированного пользователя (выдается при регистрации нового пользователя).
- ```--username USERNAME``` - Имя пользователя (указывается при регистрации нового пользователя). Если не указано то генерируется чат-сервером.
- ```--message MESSAGE``` - Собщение отправляемое в чат.
- ```--debug``` - Включить режим отладки.

# Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
