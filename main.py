import uvloop
from aiohttp import web
from dotenv.main import load_dotenv

from app.app import init_app


load_dotenv()


def main() -> None:
    uvloop.install()
    app = init_app()
    web.run_app(app, host=app['config'].HOST, port=app['config'].PORT)


if __name__ == '__main__':
    main()
