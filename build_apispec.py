#!/usr/bin/env python3
import argparse
import json

from apispec.yaml_utils import YAMLDumper
from yaml import dump as yaml_dump

from example_web_server.spec import spec

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument('-j', '--json', action='store_true', default=False)


def main():
    args = parser.parse_args()
    if args.json:
        print(json.dumps(spec.to_dict(), ensure_ascii=False))
    else:
        print(yaml_dump(spec.to_dict(), Dumper=YAMLDumper, allow_unicode=True))


if __name__ == '__main__':
    main()
