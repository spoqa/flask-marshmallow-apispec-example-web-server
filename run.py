#!/usr/bin/env python3
import argparse

from example_web_server.wsgi import create_wsgi_app

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument('-H', '--host', default='0.0.0.0', help='Address to bind')
parser.add_argument(
    '-p',
    '--port',
    type=int,
    default=8080,
    help='Port number to bind',
)


def main():
    args = parser.parse_args()
    wsgi_app = create_wsgi_app()
    wsgi_app.run(host=args.host, port=args.port, debug=True)


if __name__ == '__main__':
    main()
