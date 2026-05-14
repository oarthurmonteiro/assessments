from typing import Protocol, List, Optional
from domain.entities import Transfer, Account

class BankRepository(Protocol):
    def get_balance(self, account_id: str) -> Optional[int]:
        """Recupera o saldo de uma conta."""
        ...

    def save_balance(self, account_id: str, amount: int) -> None:
        """Atualiza o saldo de uma conta."""
        ...

    def add_to_ledger(self, transfer: Transfer) -> None:
        """Registra uma nova transferência no livro base."""
        ...

    def get_statement(self, account_id: str) -> List[Transfer]:
        """Recupera o histórico de transferências de uma conta."""
        ...