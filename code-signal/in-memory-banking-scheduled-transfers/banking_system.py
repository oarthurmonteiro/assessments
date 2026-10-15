import itertools
from enum import StrEnum
from heapq import heapify, heappop


class PaymentStatus(StrEnum):
    SCHEDULED = "scheduled" # exists, not yet accepted
    ACCEPTED = "accepted" # waiting for `due_time`
    EXECUTED = "executed"
    EXPIRED = "expired" # came due unaccepted
    FAILED = "failed" # came due, insufficient funds


class Payment:
    def __init__(
        self,
        id: str,
        payer_id: str,
        recipient_id: str,
        amount: int,
        due_time: int,
    ):
        self.id = id
        self.payer_id = payer_id
        self.recipient_id = recipient_id
        self.amount = amount
        self.due_time = due_time
        self.status = PaymentStatus.SCHEDULED

    def accept(self):
        if self.status != PaymentStatus.SCHEDULED:
            return False

        self.status = PaymentStatus.ACCEPTED
        return True

    def expire(self):
        if self.status != PaymentStatus.SCHEDULED:
            return False

        self.status = PaymentStatus.EXPIRED
        return True

    def execute(self):
        if self.status != PaymentStatus.ACCEPTED:
            return False

        self.status = PaymentStatus.EXECUTED
        return True

    def fail(self):
        if self.status != PaymentStatus.ACCEPTED:
            return False

        self.status = PaymentStatus.FAILED
        return True


class Account:
    def __init__(self, id: str):
        self.id = id
        self.balance = 0
        self.spendings = 0

    def debit(self, amount: int) -> bool:
        if amount <= 0 or amount > self.balance:
            return False

        self.balance -= amount
        self.spendings += amount
        return True

    def credit(self, amount: int) -> bool:
        if amount <= 0:
            return False

        self.balance += amount
        return True


class AccountRepository:
    def __init__(self):
        self._accounts: dict[str, Account] = {}

    def exists(self, account_id: str) -> bool:
        return account_id in self._accounts

    def delete(self, account_id: str) -> bool:
        if self.exists(account_id):
            del self._accounts[account_id]
            return True

        return False

    def create(self, account_id: str) -> bool:
        if self.exists(account_id):
            return False

        self._accounts[account_id] = Account(account_id)
        return True

    def get(self, account_id: str) -> Account | None:
        return self._accounts.get(account_id)

    def get_all(self) -> list[Account]:
        return list(self._accounts.values())


class PaymentRepository:
    def __init__(self):
        self._payments: dict[str, Payment] = {}
        self._ids = itertools.count(1)

    def next_id(self) -> str:
        return str(next(self._ids))

    def save(self, payment: Payment) -> None:
        self._payments[payment.id] = payment

    def get(self, payment_id: str) -> Payment | None:
        return self._payments.get(payment_id)

    # Could be a queue with the accepted items in order of timestamp(creation time or, how the id are sequential, ordered by id)
    def accepted(self) -> list[Payment]:
        return [t for t in self._payments.values() if t.status == PaymentStatus.ACCEPTED]

    def get_by_account_id(self, account_id: str) -> list[Payment]:
        return [
            t for t in self._payments.values()
            if t.payer_id == account_id or t.recipient_id == account_id
        ]

class BankingSystem:
    def __init__(self):
        self._accounts = AccountRepository()
        self._payments = PaymentRepository()

    def top_spenders(self, timestamp: int, n) -> list[str]:
        self._process_accepted_payments(timestamp)
        heap = [(-a.spendings,a.id) for a in self._accounts.get_all()]
        heapify(heap)
        spenders = []
        n = min(n, len(heap))
        for _ in range(n):
            spendings, id = heappop(heap)
            spenders.append(f"{id}({-spendings})")

        return spenders

    def get_balance(self, timestamp: int, account_id: str) -> int|None:
        self._process_accepted_payments(timestamp)
        account = self._accounts.get(account_id)
        return account.balance if account else None

    def create_account(self, timestamp: int, account_id: str) -> bool:
        self._process_accepted_payments(timestamp)
        return self._accounts.create(account_id)

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int|None:
        self._process_accepted_payments(timestamp)
        account = self._accounts.get(account_id)
        if account is None:
            return None

        if not account.credit(amount):
            return None

        return account.balance

    def transfer(self, timestamp: int, from_id: str, to_id: str, amount: int) -> int|None:
        self._process_accepted_payments(timestamp)
        if from_id == to_id:
            return None

        sender = self._accounts.get(from_id)
        recipient = self._accounts.get(to_id)
        if sender is None or recipient is None:
            return None

        if not sender.debit(amount):
            return None

        recipient.credit(amount)
        return sender.balance

    def schedule_payment(
        self,
        timestamp: int,
        payer_id: str,
        recipient_id: str,
        amount: int,
        due_time: int
    ) -> str|None:
        self._process_accepted_payments(timestamp)
        if payer_id == recipient_id: return None
        if amount <= 0: return None
        if due_time <= timestamp: return None

        sender = self._accounts.get(payer_id)
        recipient = self._accounts.get(recipient_id)
        if sender is None or recipient is None:
            return None

        payment = Payment(
            self._payments.next_id(),
            payer_id, recipient_id,
            amount, due_time
        )
        self._payments.save(payment)
        return payment.id

    def accept_payment(self, timestamp: int, recipient_id: str, payment_id: str) -> bool:
        self._process_accepted_payments(timestamp)
        payment = self._payments.get(payment_id)
        if not payment: return False
        if payment.recipient_id != recipient_id: return False
        if payment.due_time <= timestamp:
            payment.expire()
            return False

        return payment.accept()

    def _process_accepted_payments(self, timestamp: int):
        for p in self._payments.accepted():
            if timestamp < p.due_time:
                continue

            sender = self._accounts.get(p.payer_id)
            receiver = self._accounts.get(p.recipient_id)

            if not sender or not receiver or not sender.debit(p.amount):
                p.fail()
                continue

            receiver.credit(p.amount)
            p.execute()

    def merge_accounts(self, timestamp: int, target_id: str, source_id: str) -> bool:
        self._process_accepted_payments(timestamp)
        if target_id == source_id: return False

        target = self._accounts.get(target_id)
        source = self._accounts.get(source_id)

        if not target or not source: return False
        target.balance += source.balance
        target.spendings += source.spendings
        self._accounts.delete(source_id)

        for p in self._payments.get_by_account_id(source_id):
            if p.payer_id == source_id:
                p.payer_id = target_id

            if p.recipient_id == source_id:
                p.recipient_id = target_id

        return True
