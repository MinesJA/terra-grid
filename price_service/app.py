from uvicorn import Config
import os
import asyncio
import falcon
import falcon.asgi
import signal
import uvicorn
from .resources.price import PriceResource
from .resources.order import OrderResource
from .db import connect, create_schema

HANDLED_SIGNALS = (
        signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
        signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
        )

def create_app():
    conn = connect()
    print(f'Connected to db {conn}')
    create_schema(conn.cursor()) 
    app = falcon.asgi.App()

    # json_handler = media.JSONHandler(
            #         loads=deserialize,
            #         )
    # extra_handlers = {
            #         'application/json': json_handler,
            #         }

    # app.req_options.media_handlers.update(extra_handlers)
    # app.resp_options.media_handlers.update(extra_handlers)

    app.add_route('/prices', PriceResource(conn))
    app.add_route('/orders', OrderResource(conn))

    return app


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    def exit(self):
        self.should_exit = True


async def main():
    print('Starting server')

    app = create_app()
    server = Server(Config(app=app)) 

    server_task = asyncio.create_task(server.serve())

    try:
        await asyncio.gather(server_task) 
    except asyncio.CancelledError:
        server.exit() 


if __name__ == "__main__":
    print(f'Grid:   Starting Grid')
    print(f'GRID:   pid {os.getpid()}: send SIGINT or SIGTERM to exit.')

    loop = asyncio.get_event_loop()
    main_task = asyncio.ensure_future(main())

    for signal in HANDLED_SIGNALS:
        loop.add_signal_handler(signal, main_task.cancel) 

    try:
        loop.run_until_complete(main_task)
    finally:
        loop.close()

    print(f'GRID:   Successfully exited Grid')

    # TODO: setup logging
    # create logging branch
    # https://docs.python.org/3/library/logging.html
