import asyncio
import argparse
from datetime import datetime
import sys


from aiofile import AIOFile


def format_message(message):
    current_datetime = datetime.now().strftime('%d.%m.%y %H:%M')
    return f'[{current_datetime}] {message}\n'


async def _get_chat_connection(host, port, log_file, attempts=1, timeout=3):
    attempts_count = 0
    reader = None
    while not reader:
        try:
            reader, _ = await asyncio.open_connection(host, port)
            success_message = 'Установлено соединение.'
            print(format_message(success_message).strip())
            await log_file.write(format_message(success_message))
        except (ConnectionRefusedError, ConnectionResetError) as err:
            if attempts_count < attempts:
                error_message = 'Нет соединения. Повторная попытка.'
                print(format_message(error_message).strip())
                await log_file.write(format_message(error_message))
                attempts_count += 1
                continue
            else:
                error_message = (
                    f'Нет соединения. '
                    f'Повторная попытка через {timeout} сек.'
                )
                print(format_message(error_message).strip())
                await log_file.write(format_message(error_message))
                await asyncio.sleep(timeout)
    return reader


async def _read_chat(reader):
    data = await reader.readline()
    message = data.decode().strip()
    print(format_message(message).strip())
    return message


async def _write_to_file(data, log_file):
    message = format_message(data)
    await log_file.write(message)


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='Chat server address.')
    parser.add_argument('-P', '--port', help='Chat server port.')
    parser.add_argument(
        '-f', '--file', default='chat_history.txt',
        help='Chat history file path.'
    )

    return parser.parse_args()


async def main():
    args = process_args()

    try:
        async with AIOFile(args.file, 'a') as afp:
            while True:
                try:
                    reader = await _get_chat_connection(
                        args.host,
                        args.port,
                        afp
                    )
                    while True:
                        data = await _read_chat(reader)
                        await _write_to_file(data, afp)
                except (ConnectionRefusedError, ConnectionResetError) as err:
                    error_message = 'Соединение потеряно.'
                    print(format_message(error_message).strip())
                    await afp.write(format_message(error_message))
                    continue
    except FileNotFoundError:
        error_value = sys.exc_info()[1]
        print(f'{error_value.strerror}: {error_value.filename}')
        sys.exit(error_value.errno)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt')
