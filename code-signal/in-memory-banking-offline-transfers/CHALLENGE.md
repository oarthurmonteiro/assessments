# In-Memory Banking System with Immediate, Offline and Deletable Transfers
Implement an in-memory banking system behind a class interface. The online assessment is split into levels that all extend the same class, and tests check the behavior required at each level. The reported operations are: creating a user, transferring money between users, making an offline transfer, and deleting a transfer. The transfer logic becomes noticeably more involved in the later levels.

The exact method names and signatures come from the assessment's interface file and were not reported. Work from an interface like the illustrative one below, and settle the semantics with the clarifying questions that follow.

```py
class BankingSystem:
    def create_user(self, user_id: str) -> bool: ...
    def transfer(self, from_id: str, to_id: str, amount: int): ...
    def offline_transfer(self, from_id: str, to_id: str, amount: int): ...
    def delete_transfer(self, transfer_id: str) -> bool: ...
```

## Constraints and Clarifications
- All state lives in memory. There is no database, file or network.
- Every level adds behavior to the same class, so a change made for a later level must not break what earlier levels already required.
- The goal is code that passes the tests clearly and correctly; heavy performance optimization is not the focus.

## Clarifying Questions
- How does money enter an account: an initial balance when the user is created, or a separate deposit operation?
- What should each operation return when it fails (unknown user, duplicate user, non-positive amount, insufficient funds, a transfer to oneself): False , None , or an exception?
- What makes an offline transfer take effect: a later explicit call, a time carried by later operations, or something else?
- Are the sender's funds reserved when an offline transfer is created, or checked only when it takes effect?
- Which transfers can be deleted: only offline transfers that have not taken effect yet, or also completed ones, which would mean reversing them? Who is allowed to delete one?
- Are amounts whole numbers in the smallest currency unit?

## Part 1 — Users and immediate transfers
Support creating users and moving money between two existing users immediately. Both balances must change together, or neither may change.

### What This Part Should Cover
- Account storage keyed by user ID, including what happens when an ID is created twice
- Validation of unknown users, non-positive amounts, self-transfers and insufficient funds
- Balance updates that are all-or-nothing, with consistent return values

## Part 2 — Offline transfers
Add offline transfers: a transfer that is accepted now but does not deliver the money to the recipient immediately. Each one needs an identifier so that it can be referred to later.

### What This Part Should Cover
- A transfer record with an identifier, both parties, the amount and a state
- A defined trigger that makes an offline transfer take effect, applied in a deterministic order
- How outstanding offline transfers interact with the sender's spendable balance and with immediate transfers

## Part 3 — Deleting a transfer
Add deleting a transfer by its identifier.

### What This Part Should Cover
- Which states can be deleted, and the result for unknown or already finished transfers
- Restoring balances correctly and exactly once
- Guaranteeing that a deleted transfer can never take effect afterwards

## What a Strong Answer Covers
- A data model in which balances can always be reconciled against the transfer records
- No money created or lost under any sequence of operations
- Failure semantics that are explicit and stay consistent across levels
- Tests or a trace that exercise the success and failure paths of every operation
- Code organized so that each new level is an extension rather than a rewrite

## Follow-up Questions
- How would you add a query that returns a user's balance as of an earlier point in time?
- A user is removed while offline transfers to or from them are still outstanding. What should happen to those transfers?
- How would the design change if several threads called these methods at the same time?
- The system must survive a restart. What would you persist, and in what order, so that no transfer is applied twice or lost?
