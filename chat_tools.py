import asyncio
import logging
from datetime import datetime


def format_message(message):
    current_datetime = datetime.now().strftime('%d.%m.%y %H:%M')
    return f'[{current_datetime}] {message}\n'


async def get_chat_connection(host, port, log_file, attempts=1, timeout=3):
    attempts_count = 0
    reader = None
    while not reader:
        try:
            reader, _ = await asyncio.open_connection(host, port)
            success_message = 'Установлено соединение.'
            logging.debug(format_message(success_message).rstrip())
            await log_file.write(format_message(success_message))
        except (ConnectionRefusedError, ConnectionResetError) as err:
            if attempts_count < attempts:
                error_message = 'Нет соединения. Повторная попытка.'
                logging.debug(format_message(error_message).rstrip())
                await log_file.write(format_message(error_message))
                attempts_count += 1
                continue
            else:
                error_message = (
                    f'Нет соединения. '
                    f'Повторная попытка через {timeout} сек.'
                )
                logging.debug(format_message(error_message).rstrip())
                await log_file.write(format_message(error_message))
                await asyncio.sleep(timeout)
    return reader


async def read_chat_message(reader):
    data = await reader.readline()
    message = data.decode().rstrip()
    logging.debug(format_message(message).rstrip())
    return message


async def write_message_to_file(data, log_file):
    message = format_message(data)
    await log_file.write(message)
