from typing import Dict, List, Optional

from domain.entities import Transfer

class InMemoryBankRepository: # Note: não precisa herdar de BankRepository
    def __init__(self):
        self._accounts = {}
        self._ledger = []

    def get_balance(self, account_id: str) -> Optional[int]:
        return self._accounts.get(account_id)

    def save_balance(self, account_id: str, amount: int) -> None:
        self._accounts[account_id] = amount

    def add_to_ledger(self, transfer: Transfer) -> None:
        self._ledger.append(transfer)

    def get_statement(self, account_id: str) -> List[Transfer]:
        return [t for t in self._ledger if t.source_id == account_id or t.destiny_id == account_id]