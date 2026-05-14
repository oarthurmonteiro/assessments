from data.repository import InMemoryBankRepository
from domain.entities import Transfer, TransferStatus
from domain.interfaces import BankRepository


class BankService:
    def __init__(self, repo: BankRepository):
        self.repo = repo

    def transfer(self, source_id: str, target_id: str, amount: int):
        # 1. Validação
        source_balance = self.repo.get_balance(source_id)
        if source_balance is None or source_balance < amount:
            raise ValueError("Saldo insuficiente ou conta inexistente")

        # 2. Criação da Entidade
        new_transfer = Transfer(source_id, target_id, amount)

        # 3. Atualização Atômica (No Ledger e nos Saldos)
        # Aqui você pode simular uma "transação"
        self.repo.save_account(source_id, source_balance - amount)
        
        target_balance = self.repo.get_balance(target_id) or 0
        self.repo.save_account(target_id, target_balance + amount)
        
        new_transfer.status = TransferStatus.COMPLETED
        self.repo.add_to_ledger(new_transfer)
        
        return new_transfer.id