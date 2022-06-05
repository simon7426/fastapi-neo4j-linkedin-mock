import argparse
import sys
from ast import arg

import uvicorn


def run(host, port):
    uvicorn.run("project:app", host=host, port=port, log_level="info", reload=True)


def parse_args(args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--host", dest="host", type=str, default="0.0.0.0")
    parser.add_argument("-p", "--port", dest="port", type=int, default=5000)
    ret = parser.parse_args(args)
    return ret


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide an argument after manage.py")
        print("Exiting...")
        sys.exit(1)
    options = parse_args(sys.argv[2:])
    if sys.argv[1] == "run":
        run(options.host, options.port)
    else:
        print(f'Invalid operation "{sys.argv[1]}".')
        print("Exiting...")
        sys.exit(1)
