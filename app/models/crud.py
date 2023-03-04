import datetime
from typing import Union, Optional, Any, Dict, List

from app.models import User, Transaction, TransactionType


class CrudMixin:
    @staticmethod
    def make_float(amount: float, transaction_type: str) -> float:
        if transaction_type.upper() == TransactionType.DEPOSIT.name:
            return float(amount)
        return float(f"-{amount}")

    @staticmethod
    def format_user(user: User) -> Dict[str, Any]:
        user_dict = user.to_dict()
        user_dict["balance"] = str(user_dict["balance"])
        return user_dict


class UserCrud(CrudMixin):
    @staticmethod
    async def get_user(user_id: int):
        return await User.get(user_id)

    @staticmethod
    async def create_user(name: str) -> User:
        user = await User.create(name=name)
        return user

    async def update_user_balance(
        self, amount: float, user_id: int, transaction_type: str
    ) -> tuple:
        amount = self.make_float(amount=amount, transaction_type=transaction_type)
        return (
            await User.update.values(balance=User.balance + amount)
            .where(User.id == user_id)
            .gino.status()
        )


class TransactionCrud:
    @staticmethod
    async def create_transaction(
        user_id: int,
        transaction_type: str,
        amount: float,
        timestamp: Optional[Union[str, datetime.datetime]] = None,
        uid: Optional[str] = None,
    ) -> Transaction:
        if not timestamp:
            timestamp = datetime.datetime.now()
        else:
            timestamp = datetime.datetime.fromisoformat(timestamp)
        transaction = await Transaction.create(
            type=transaction_type,
            amount=amount,
            timestamp=timestamp,
            user_id=user_id,
            uid=uid,
        )
        return transaction

    @staticmethod
    async def get_transaction(transaction_uid: str) -> Optional[Transaction]:
        return await Transaction.query.where(
            Transaction.uid == transaction_uid
        ).gino.first()

    @staticmethod
    async def get_user_transactions(
        user_id: int, timestamp: Optional[datetime.datetime] = None
    ) -> List[Transaction]:
        if not timestamp:
            timestamp = datetime.datetime.now()
        return (
            await Transaction.query.where(Transaction.user_id == user_id)
            .where(Transaction.timestamp < timestamp)
            .gino.all()
        )