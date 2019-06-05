import asyncio
import argparse


async def _get_chat_connection(host, port, attempts=1, timeout=3):
    attempts_count = 0
    reader = None
    while not reader:
        try:
            reader, _ = await asyncio.open_connection(host, port)
            print('Установлено соединение.')
        except (ConnectionRefusedError, ConnectionResetError) as err:
            if attempts_count < attempts:
                print('Нет соединения. Повторная попытка.')
                attempts_count += 1
                continue
            else:
                print(
                    f'Нет соединения. Повторная попытка через {timeout} сек.'
                )
                await asyncio.sleep(timeout)
    return reader


async def _read_chat(reader):
    while True:
        data = await reader.readline()
        print(data.decode().strip())


async def main():
    args = process_args()
    while True:
        try:
            reader = await _get_chat_connection(args.host, args.port)
            await _read_chat(reader)
        except (ConnectionRefusedError, ConnectionResetError) as err:
            print('Соединение потеряно.')
            continue


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='Server address.')
    parser.add_argument('-P', '--port', help='Server port.')

    return parser.parse_args()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt')
