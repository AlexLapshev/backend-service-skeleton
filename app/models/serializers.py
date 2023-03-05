from typing import Dict, Any, Union, List

from app.models import User, Transaction


class BaseSerializer:
    @staticmethod
    def serialize(model: Union[User, Transaction], fields: List[str]) -> Dict[str, Any]:
        model_dict = model.to_dict()
        for f in fields:
            model_dict[f] = str(model_dict[f])
        return model_dict


class UserSerializer(BaseSerializer):
    def serialize(self, user: User) -> Dict[str, Any]:
        return super().serialize(user, ["balance"])


class TransactionSerializer(BaseSerializer):
    def serialize(self, transaction: Transaction) -> Dict[str, Any]:
        t_dict = super().serialize(transaction, ["amount", "uid", "timestamp"])
        t_dict["type"] = t_dict["type"].name
        return t_dict
