"""
Reference variant of banking_system.py, for comparison only — not meant to
replace your implementation. Same public interface and test suite apply.
"""

import functools
import heapq
import itertools
from dataclasses import dataclass
from enum import StrEnum


class PaymentStatus(StrEnum):
    SCHEDULED = "scheduled"
    ACCEPTED = "accepted"
    EXECUTED = "executed"
    EXPIRED = "expired"
    FAILED = "failed"


class Payment:
    def __init__(self, id: str, payer_id: str, recipient_id: str, amount: int, due_time: int):
        self.id = id
        self.payer_id = payer_id
        self.recipient_id = recipient_id
        self.amount = amount
        self.due_time = due_time
        self.status = PaymentStatus.SCHEDULED

    def accept(self) -> bool:
        if self.status != PaymentStatus.SCHEDULED:
            return False

        self.status = PaymentStatus.ACCEPTED
        return True

    def expire(self) -> bool:
        if self.status != PaymentStatus.SCHEDULED:
            return False

        self.status = PaymentStatus.EXPIRED
        return True

    def execute(self) -> bool:
        if self.status != PaymentStatus.ACCEPTED:
            return False

        self.status = PaymentStatus.EXECUTED
        return True

    def fail(self) -> bool:
        if self.status != PaymentStatus.ACCEPTED:
            return False

        self.status = PaymentStatus.FAILED
        return True


@dataclass
class Transaction:
    timestamp: int
    counterparty_id: str | None  # None for a deposit: money entered from outside the system
    amount: int
    direction: str  # "in" or "out"


class Account:
    def __init__(self, account_id: str):
        self.id = account_id
        self.balance = 0
        self.outgoing_total = 0
        self.history: list[Transaction] = []

    def debit(self, amount: int, timestamp: int, counterparty_id: str) -> bool:
        if amount <= 0 or amount > self.balance:
            return False

        self.balance -= amount
        self.outgoing_total += amount
        self.history.append(Transaction(timestamp, counterparty_id, amount, "out"))
        return True

    def credit(self, amount: int, timestamp: int, counterparty_id: str | None) -> bool:
        if amount <= 0:
            return False

        self.balance += amount
        self.history.append(Transaction(timestamp, counterparty_id, amount, "in"))
        return True


class AccountRepository:
    def __init__(self):
        self._accounts: dict[str, Account] = {}

    def exists(self, account_id: str) -> bool:
        return account_id in self._accounts

    def create(self, account_id: str) -> bool:
        if self.exists(account_id):
            return False

        self._accounts[account_id] = Account(account_id)
        return True

    def get(self, account_id: str) -> Account | None:
        return self._accounts.get(account_id)

    def get_all(self) -> list[Account]:
        return list(self._accounts.values())

    def delete(self, account_id: str) -> bool:
        if not self.exists(account_id):
            return False

        del self._accounts[account_id]
        return True


class PaymentRepository:
    def __init__(self):
        self._payments: dict[str, Payment] = {}
        self._ids = itertools.count(1)
        self._due_heap: list[tuple[int, int, Payment]] = []

    def next_id(self) -> str:
        return str(next(self._ids))

    def save(self, payment: Payment) -> None:
        self._payments[payment.id] = payment
        heapq.heappush(self._due_heap, (payment.due_time, int(payment.id), payment))

    def get(self, payment_id: str) -> Payment | None:
        return self._payments.get(payment_id)

    def get_by_account_id(self, account_id: str) -> list[Payment]:
        return [
            p for p in self._payments.values()
            if p.payer_id == account_id or p.recipient_id == account_id
        ]

    def pop_due(self, timestamp: int) -> list[Payment]:
        due = []
        while self._due_heap and self._due_heap[0][0] <= timestamp:
            _, _, payment = heapq.heappop(self._due_heap)
            due.append(payment)

        return due



def processes_due_payments(method):
    @functools.wraps(method)
    def wrapper(self, timestamp, *args, **kwargs):
        self._process_due_payments(timestamp)
        return method(self, timestamp, *args, **kwargs)
    return wrapper


class BankingSystem:
    def __init__(self):
        self._accounts = AccountRepository()
        self._payments = PaymentRepository()

    def _process_due_payments(self, timestamp: int) -> None:
        for payment in self._payments.pop_due(timestamp):
            if payment.status == PaymentStatus.SCHEDULED:
                payment.expire()
                continue

            sender = self._accounts.get(payment.payer_id)
            recipient = self._accounts.get(payment.recipient_id)
            if (
                sender is None
                or recipient is None
                or not sender.debit(payment.amount, timestamp, payment.recipient_id)
            ):
                payment.fail()
                continue

            recipient.credit(payment.amount, timestamp, payment.payer_id)
            payment.execute()

    @processes_due_payments
    def create_account(self, timestamp: int, account_id: str) -> bool:
        return self._accounts.create(account_id)

    @processes_due_payments
    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        account = self._accounts.get(account_id)
        if account is None or not account.credit(amount, timestamp, None):
            return None

        return account.balance

    @processes_due_payments
    def get_balance(self, timestamp: int, account_id: str) -> int | None:
        account = self._accounts.get(account_id)
        return account.balance if account else None

    @processes_due_payments
    def transfer(self, timestamp: int, from_id: str, to_id: str, amount: int) -> int | None:
        if from_id == to_id:
            return None

        sender = self._accounts.get(from_id)
        recipient = self._accounts.get(to_id)
        if sender is None or recipient is None:
            return None

        if not sender.debit(amount, timestamp, to_id):
            return None

        recipient.credit(amount, timestamp, from_id)
        return sender.balance

    @processes_due_payments
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        ranked = sorted(self._accounts.get_all(), key=lambda a: (-a.outgoing_total, a.id))
        return [f"{a.id}({a.outgoing_total})" for a in ranked[:n]]

    @processes_due_payments
    def schedule_payment(
        self, timestamp: int, payer_id: str, recipient_id: str, amount: int, due_time: int
    ) -> str | None:
        if payer_id == recipient_id or amount <= 0 or due_time <= timestamp:
            return None

        if not self._accounts.exists(payer_id) or not self._accounts.exists(recipient_id):
            return None

        payment = Payment(self._payments.next_id(), payer_id, recipient_id, amount, due_time)
        self._payments.save(payment)
        return payment.id

    @processes_due_payments
    def accept_payment(self, timestamp: int, recipient_id: str, payment_id: str) -> bool:
        payment = self._payments.get(payment_id)
        if payment is None or payment.recipient_id != recipient_id:
            return False

        return payment.accept()

    @processes_due_payments
    def merge_accounts(self, timestamp: int, target_id: str, source_id: str) -> bool:
        if target_id == source_id:
            return False

        target = self._accounts.get(target_id)
        source = self._accounts.get(source_id)
        if target is None or source is None:
            return False

        target.balance += source.balance
        target.outgoing_total += source.outgoing_total
        target.history = sorted(target.history + source.history, key=lambda t: t.timestamp)

        for payment in self._payments.get_by_account_id(source_id):
            if payment.payer_id == source_id:
                payment.payer_id = target_id
            if payment.recipient_id == source_id:
                payment.recipient_id = target_id

        self._accounts.delete(source_id)
        return True
