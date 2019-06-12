# CLI клиент для подключения к чату.

Задача: написать программу для подключения к чату через командную строку.  
Функции программы:
1. Подключается к указанному чат серверу;
2. Сохраняет историю переписки;
3. Отправляет сообщения в чат.

## Как установить

Для работы микросервиса нужен Python версии не ниже 3.7+.  
Также в программе используются следующие сторонние библиотеки:
- aiofiles [https://github.com/Tinche/aiofiles](https://github.com/Tinche/aiofiles);
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