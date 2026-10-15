import itertools
from enum import StrEnum
from typing import cast


class TransferStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Transfer:
    def __init__(self, transfer_id: str, from_id: str, to_id: str, amount: int):
        self.id = transfer_id
        self.from_user = from_id
        self.to_user = to_id
        self.amount = amount
        self.status = TransferStatus.PENDING

    def cancel(self) -> bool:
        if self.status in (TransferStatus.COMPLETED, TransferStatus.CANCELLED):
            return False

        self.status = TransferStatus.CANCELLED
        return True

    def proceed(self) -> bool:
        if self.status in (TransferStatus.COMPLETED, TransferStatus.CANCELLED):
            return False

        self.status = TransferStatus.COMPLETED
        return True


class Account:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.balance = 0

    def debit(self, amount: int) -> bool:
        if amount <= 0 or amount > self.balance:
            return False

        self.balance -= amount
        return True

    def credit(self, amount: int) -> bool:
        if amount <= 0:
            return False

        self.balance += amount
        return True


class UserRepository:
    def __init__(self):
        self._accounts: dict[str, Account] = {}

    def exists(self, user_id: str) -> bool:
        return user_id in self._accounts

    def create(self, user_id: str) -> bool:
        if self.exists(user_id):
            return False

        self._accounts[user_id] = Account(user_id)
        return True

    def get(self, user_id: str) -> Account | None:
        return self._accounts.get(user_id)


class TransferRepository:
    def __init__(self):
        self._transfers: dict[str, Transfer] = {}
        self._ids = itertools.count(1)

    def next_id(self) -> str:
        return str(next(self._ids))

    def save(self, transfer: Transfer) -> None:
        self._transfers[transfer.id] = transfer

    def get(self, transfer_id: str) -> Transfer | None:
        return self._transfers.get(transfer_id)

    def pending(self) -> list[Transfer]:
        return [t for t in self._transfers.values() if t.status == TransferStatus.PENDING]


class BankingSystem:
    def __init__(self):
        self._users = UserRepository()
        self._transfers = TransferRepository()

    def create_user(self, user_id: str) -> bool:
        return self._users.create(user_id)

    def deposit(self, user_id: str, amount: int) -> bool:
        account = self._users.get(user_id)
        if account is None:
            return False

        return account.credit(amount)

    def get_balance(self, user_id: str) -> int | None:
        account = self._users.get(user_id)
        return account.balance if account else None

    def transfer(self, from_id: str, to_id: str, amount: int) -> bool:
        if from_id == to_id:
            return False

        sender = self._users.get(from_id)
        recipient = self._users.get(to_id)
        if sender is None or recipient is None:
            return False

        if not sender.debit(amount):
            return False

        transfer = Transfer(self._transfers.next_id(), from_id, to_id, amount)
        recipient.credit(amount)
        transfer.proceed()
        self._transfers.save(transfer)
        return True

    def offline_transfer(self, from_id: str, to_id: str, amount: int) -> str | None:
        if from_id == to_id:
            return None

        sender = self._users.get(from_id)
        recipient = self._users.get(to_id)
        if sender is None or recipient is None:
            return None

        if not sender.debit(amount):
            return None

        transfer = Transfer(self._transfers.next_id(), from_id, to_id, amount)
        self._transfers.save(transfer)
        return transfer.id

    def process_offline_transfers(self) -> None:
        for transfer in self._transfers.pending():
            recipient = self._users.get(transfer.to_user)
            if not recipient: continue
            recipient.credit(transfer.amount)
            transfer.proceed()

    def delete_transfer(self, transfer_id: str) -> bool:
        transfer = self._transfers.get(transfer_id)
        if transfer is None:
            return False

        if not transfer.cancel():
            return False

        sender = cast("Account", self._users.get(transfer.from_user))
        sender.credit(transfer.amount)
        return True
