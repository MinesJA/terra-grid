import os
from termcolor import colored, cprint
import datetime
import asyncio
import argparse
import sys
import schedule
import signal

from node.services.rule_executor import execute_transaction

HANDLED_SIGNALS = (
        signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
        signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
        )

def parse_args(args):
    return create_parser().parse_args(args)

def create_parser():
    parser = argparse.ArgumentParser(description='Start a node')
    # parser.add_argument('--name', '-n')
    parser.add_argument('--id', '-i', type=int)
    # parser.add_argument('--token', '-t')
    # parser.add_argument('--host', '-s')
    # parser.add_argument('--port', '-p', type=int)
    return parser


ARGS = parse_args(sys.argv[1:])

def execute(node_id, i, start_at):
   next_timestamp = start_at + datetime.timedelta(minutes=i) 
   execute_transaction(node_id, next_timestamp)
    
async def scheduler(node_id):
    # schedule.every().second.do(execute_transaction) 
    start_at = datetime.datetime.now().replace(second=0, microsecond=0)
    for i in range(1,100):
        # schedule.run_pending()
        await asyncio.sleep(1)
        execute(node_id, i, start_at)

async def main():
    cprint(f"Starting up node", "red", "on_white", attrs=["reverse", "bold"])
    scheduler_task = asyncio.create_task(scheduler(ARGS.id))

    try:
        await asyncio.gather(scheduler_task) 
    except asyncio.CancelledError:
        scheduler_task.cancel() 

if __name__ == "__main__":
    print(f'Node:   Starting Node')
    print(f'Node:   pid {os.getpid()}: send SIGINT or SIGTERM to exit.')

    loop = asyncio.get_event_loop()
    main_task = asyncio.ensure_future(main())

    for signal in HANDLED_SIGNALS:
        loop.add_signal_handler(signal, main_task.cancel) 

    try:
        loop.run_until_complete(main_task)
    finally:
        loop.close()

    print(f'Node:   Successfully exited Node')

    # TODO: setup logging
    # create logging branch
    # https://docs.python.org/3/library/logging.html
