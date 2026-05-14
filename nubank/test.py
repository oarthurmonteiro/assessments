    class Account():
        def __init__(self, id):
            self.id = id
            self.balance = 0
            self.transactions_amount = 0
            
    class Transfer():
        def __init__(self, id, amount, source_account_id, destiny_account_id, created_at):
            self.id = id
            self.amount = amount
            self.source_account_id = source_account_id
            self.destiny_account_id = destiny_account_id
            self.created_at = created_at
            self.expire_at = created_at + 86400000
            self.isDone = False 

    class BankSimulation():
        def __init__(self):
            self.accounts = {}
            self.transfers = {}
            self.transfers_length = 0
        
        def does_account_exists(self, account_id) -> bool:
            return account_id in self.accounts
        
        def create_account(self, timestamp, account_id) -> bool:
            if self.does_account_exists(account_id):
                return False
            
            self.accounts[account_id] = {
                    'name': account_id,
                    'balance': 0,
                    'created_at': timestamp,
                    'updated_at': timestamp,
                    'transactions_amount': 0
            }
            
            return True
        
        def deposit(self, timestamp, account_id, amount) -> None | int:
            if not self.does_account_exists(account_id):
                return None
            
            account = self.accounts[account_id]
            account['balance'] += amount
            account['transactions_amount'] += amount
            return account['balance']
        
        def pay(self, timestamp, account_id, amount) -> None | int:
            if not self.does_account_exists(account_id):
                return None
            
            if self.accounts[account_id]['balance'] < amount:
                return None
            
            account = self.accounts[account_id]
            account['balance'] -= amount
            account['transactions_amount'] += amount
            return account['balance']
        
        def top_activity(self, timestamp, n) -> list[str]:
            ranked_accounts = sorted(
                self.accounts.values(), 
                key=lambda x: (-x['transactions_amount'], x['name'])
            )
            
            result = []
            for account in ranked_accounts[:n]:
                result.append(f"{account['name']}({account['transactions_amount']})")
                
            return result
        
        def transfer(self, 
                    timestamp, 
                    source_account_id, 
                    destiny_account_id,
                    amount) -> None | str:
            if source_account_id == destiny_account_id:
                return None
            
            if not (self.does_account_exists(source_account_id) and 
                    self.does_account_exists(destiny_account_id)):
                return None
            
            source_account = self.accounts[source_account_id]
            if source_account['balance'] < amount:
                return None
            
            self.transfers_length += 1
            transfer_id = f"transfer{self.transfers_length}"
            
            self.transfers[transfer_id] = Transfer(
                transfer_id,
                amount,
                source_account_id,
                destiny_account_id,
                timestamp
            )
            
            account = self.accounts[source_account_id]
            account['balance'] -= amount
            account['transactions_amount'] += amount
            
            return transfer_id
        
        def accept_transfer(self,
                            timestamp,
                            account_id,
                            transfer_id) -> bool:
            if not transfer_id in self.transfers:
                return False
            
            transfer = self.transfers[transfer_id]
            if transfer.destiny_account_id != account_id or transfer.isDone:
                return False
            
            if timestamp > transfer.expire_at:
                account = self.accounts[transfer.source_account_id]
                account['balance'] += transfer.amount
                # account.transactions_amount -= transfer.amount
                transfer.isDone = True
                return False
            
            
            account = self.accounts[account_id]
            account['balance'] += transfer.amount
            account['transactions_amount'] += transfer.amount
            return True
        
        

