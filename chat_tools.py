import asyncio
from contextlib import asynccontextmanager
import logging
from datetime import datetime


async def _get_network_streams(host, port, log_file, attempts=1, timeout=3):
    attempts_count = 0
    reader = None
    writer = None
    while not reader:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            success_message = 'Установлено соединение.'
            logging.debug(success_message)
            await write_message_to_file(success_message, log_file)
        except (ConnectionRefusedError, ConnectionResetError) as err:
            if attempts_count < attempts:
                error_message = 'Нет соединения. Повторная попытка.'
                logging.debug(error_message)
                await log_file.write(error_message)
                attempts_count += 1
                continue
            else:
                error_message = (
                    f'Нет соединения. '
                    f'Повторная попытка через {timeout} сек.'
                )
                logging.debug(error_message)
                await log_file.write(error_message)
                await asyncio.sleep(timeout)
    return reader, writer


@asynccontextmanager
async def get_chat_connection(host, port, log_file):
    reader, writer = await _get_network_streams(host, port, log_file)
    try:
        yield reader, writer
    finally:
        writer.close()


async def read_chat_message(reader):
    data = await reader.readline()
    message = data.decode().rstrip()
    logging.debug(message)
    return message


async def write_message_to_file(message, log_file):
    current_datetime = datetime.now().strftime('%d.%m.%y %H:%M')
    line = f'[{current_datetime}] {message}\n'
    await log_file.write(line)
