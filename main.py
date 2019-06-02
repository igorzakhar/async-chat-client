import asyncio
import argparse


async def tcp_client(host, port):
    reader, _ = await asyncio.open_connection(host, port)

    while True:
        data = await reader.readline()
        print(data.decode().strip())


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host')
    parser.add_argument('-P', '--port')

    return parser.parse_args()


if __name__ == '__main__':
    args = process_args()
    try:
        asyncio.run(tcp_client(args.host, args.port))
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt')
