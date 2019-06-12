import asyncio
import argparse
import logging
import os
import sys

from aiofile import AIOFile
from chat_tools import get_chat_connection, write_message_to_file


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logging.getLogger('asyncio').setLevel(logging.WARNING)


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host', default=os.getenv('CHAT_HOST', 'minechat.dvmn.org'),
        help='Chat server address.'
    )
    parser.add_argument(
        '--port', default=os.getenv('CHAT_READ_PORT', 5000),
        help='Chat server port.'
    )
    parser.add_argument(
        '--history', default='chat.history',
        help='Chat history file path.'
    )

    return parser.parse_args()


async def read_chat_message(reader):
    data = await reader.readline()
    message = data.decode().rstrip()
    logging.debug(message)
    return message


async def read_messages_from_chat(host, port, log_file):
    async with get_chat_connection(host, port, log_file) as (reader, writer):
        while True:
            message = await read_chat_message(reader)
            await write_message_to_file(message, log_file)


async def main():
    args = process_args()

    try:
        async with AIOFile(args.history, 'a') as afp:
            while True:
                try:
                    await read_messages_from_chat(args.host, args.port, afp)
                except (ConnectionRefusedError, ConnectionResetError) as err:
                    error_message = 'Соединение потеряно.'
                    logging.debug(error_message)
                    await write_message_to_file(error_message, afp)
                    continue
    except FileNotFoundError:
        error_value = sys.exc_info()[1]
        logging.debug(f'{error_value.strerror}: {error_value.filename}')
        sys.exit(error_value.errno)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt')
