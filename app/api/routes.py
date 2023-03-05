from datetime import datetime

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from asyncpg import CheckViolationError

from app.models import User
from app.models.crud import UserCrud, TransactionCrud
from app.models.queries import create_balance_query
from app.models.serializers import UserSerializer, TransactionSerializer


async def add_user(request: Request) -> Response:
    request_json = await request.json()
    user = await UserCrud().create_user(**request_json)
    return web.json_response(UserSerializer(obj=user).serialize(), status=201)


async def get_user(request: Request) -> Response:
    user_id = int(request.match_info["id"])
    timestamp = request.query.get("date")
    if timestamp:
        timestamp = datetime.fromisoformat(timestamp)
    row = await request.app["db"].first(create_balance_query(user_id=user_id, timestamp=timestamp))
    if not row:
        return web.json_response(status=404)

    user = User(
        id=row[0],
        name=row[1],
        balance=row[-1]
    )
    return web.json_response(UserSerializer(obj=user).serialize(), status=200)


async def add_transaction(request: Request) -> Response:
    request_json = await request.json()
    amount = request_json["amount"]
    user_id = request_json["user_id"]
    transaction_type = request_json["type"]
    async with request.app["db"].transaction() as tx:
        try:
            res, _ = await UserCrud().update_user_balance(
                amount=amount,
                user_id=user_id,
                transaction_type=transaction_type,
            )
        except CheckViolationError:
            return web.json_response(status=402)

        if res != "UPDATE 1":
            await tx.raise_rollback()

        transaction = await TransactionCrud().create_transaction(
            amount=amount,
            user_id=user_id,
            transaction_type=transaction_type,
            timestamp=request_json["timestamp"],
            uid=request_json["uid"],
        )
        return web.json_response(TransactionSerializer(obj=transaction).serialize(), status=201)


async def get_transaction(request: Request) -> Response:
    transaction_uid = request.match_info["uid"]
    transaction = await TransactionCrud().get_transaction(
        transaction_uid=transaction_uid
    )
    if not transaction:
        return web.json_response(status=404)
    return web.json_response(TransactionSerializer(obj=transaction).serialize(), status=200)


def add_routes(app):
    app.router.add_route("GET", r"/v1/user/{id}", get_user, name="get_user")
    app.router.add_route("POST", r"/v1/user", add_user, name="add_user")
    app.router.add_route(
        "GET", r"/v1/transaction/{uid}", get_transaction, name="get_transaction"
    )
    app.router.add_route(
        "POST", r"/v1/transaction", add_transaction, name="add_transaction"
    )
