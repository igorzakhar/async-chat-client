import asyncio
import argparse
import json
import logging
import os
import sys

import aioconsole
from chat_tools import get_chat_connection

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
        '--token', default=os.getenv('CHAT_TOKEN', ''),
        help='User token'
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='Enable debug mode'
    )

    parser.add_argument('--username', help='Username')
    parser.add_argument('--message', help='Message')
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


async def is_authorized(reader, writer, token):
    data = await read_message(reader)
    await write_message(writer, f'{token}\n')
    data = await read_message(reader)
    if not json.loads(data):
        return False
    return True


async def register(reader, writer, username):
    await read_message(reader)
    await write_message(writer)
    await read_message(reader)

    if username:
        await write_message(writer, f'{username}\n')
    else:
        await write_message(writer)
    account_info = await read_message(reader)
    return json.loads(account_info)


async def submit_message(writer, message):
    await write_message(writer, f'{message}\n\n')


async def send_message_loop(writer):
    while True:
        message = await aioconsole.ainput('>>> ')
        await submit_message(writer, message)


async def main():
    args = process_args()
    host = args.host
    port = args.port
    token = args.token
    username = args.username
    message = args.message

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with get_chat_connection(host, port) as (reader, writer):
        try:
            if token:
                authorized = await is_authorized(reader, writer, token)
                if not authorized:
                    print(
                        'Неизвестный токен.'
                        'Поверьте его или зарегистрируйте заново.'
                    )
                    return
            else:
                await register(reader, writer, username)
            if message:
                await submit_message(writer, message)
            else:
                await send_message_loop(writer)
        except (ConnectionRefusedError, ConnectionResetError) as err:
            log.exception(f'{err.strerror}', exc_info=False)
            sys.exit(err.errno)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt')
