import asyncio
import argparse
import json
import logging
import os

import aioconsole


log = logging.getLogger('sender')
logging.getLogger('asyncio').setLevel(logging.WARNING)


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host', default=os.getenv('CHAT_HOST', 'minechat.dvmn.org'),
        help='Chat server address.'
    )
    parser.add_argument(
        '--port', default=os.getenv('CHAT_WRITE_PORT', 5050),
        help='Chat server port.'
    )
    parser.add_argument(
        '--token', default=os.getenv('CHAT_TOKEN', '')
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='Enable debug mode'
    )
    return parser.parse_args()


async def read_message(reader):
    data = await reader.readline()
    message = data.decode().rstrip('\n')
    log.debug(message)
    return message


async def write_message(writer, message=None):
    if not message:
        message = '\n'
    writer.write(message.encode())
    log.debug(f'Sent message: {message!r}')
    await writer.drain()


async def main():
    args = process_args()
    token = args.token

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    reader, writer = await asyncio.open_connection(args.host, args.port)

    if token:
        data = await read_message(reader)
        await write_message(writer, f'{token}\n')
        data = await read_message(reader)
        if not json.loads(data):
            print(
                'Неизвестный токен. Поверьте его или зарегистрируйте заново.'
            )
        else:
            data = await read_message(reader)

    else:
        data = await read_message(reader)
        await write_message(writer)
        data = await read_message(reader)
        username = await aioconsole.ainput('>>> ')
        if username:
            await write_message(writer, f'{username}\n')
            await read_message(reader)
            await read_message(reader)

        else:
            await write_message(writer)
            await read_message(reader)
            await read_message(reader)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt')
