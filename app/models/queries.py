import datetime
from typing import Optional

from app.models import TransactionType

balance_query = """(select coalesce(sum(t.amount), 0.00)
from transactions t 
where t."type" = '{}' and 
t.user_id = {} and
t."timestamp" < '{}'
)
"""


def create_balance_query(user_id: int, timestamp: Optional[datetime.datetime] = None):
    if not timestamp:
        timestamp = datetime.datetime.now()
    return \
        f"""select distinct u.id, u."name", u.balance, 
    {balance_query.format(TransactionType.DEPOSIT.name, user_id, str(timestamp))}
    -
    {balance_query.format(TransactionType.WITHDRAW.name, user_id, str(timestamp))}
    as balance_on_date
    from transactions t2
    inner join 
    users u on t2.user_id = u.id 
    """
