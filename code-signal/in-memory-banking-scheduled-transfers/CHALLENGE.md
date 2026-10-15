# In-Memory Banking System: Transfers, Top Spenders, Scheduled Payments, Account Merges

Implement an in-memory banking system that grows over four levels. Each level adds requirements on top of the previous ones, and everything from earlier levels must keep working, so the design choices you make in Level 1 decide how painful the later levels are. Every operation receives the current `timestamp` as its first argument.

## Clarifying Questions
- Are timestamps integers, and do operations always arrive in increasing timestamp order?
- What should each operation return on success and on failure: a boolean, the resulting balance, a null value?
- Are amounts integers, and are they always positive?

## Part 1 — Basic banking operations
Support these operations:
```
create_account(timestamp, account_id)
deposit(timestamp, account_id, amount)
transfer(timestamp, source_account_id, target_account_id, amount)
```
Creating an account that already exists, depositing into or transferring between accounts that do not exist, and transferring more than the source account holds are invalid operations.


### Clarifying Questions for this Part
- Can an account transfer money to itself?
- Does a failed operation leave any trace, for example an entry in the account's history?
### What This Part Should Cover
- Validation of every failure case before any state changes.
- An account representation that can grow to support the later levels.
- Consistent, documented return values.

## Part 2 — Top spenders
Add:
```
top_spenders(timestamp, n)
```
It ranks accounts by the total value of their outgoing transactions and returns the top n.

### Clarifying Questions for this Part
- How are ties broken?
- What is the output format: account ids only, or ids together with their totals?
- If n exceeds the number of accounts, are all accounts returned? Do accounts with no outgoing value appear?
- Which transactions count as outgoing: only transfers, or also scheduled payments once they execute (Part 3)?

### What This Part Should Cover
- A precise definition of outgoing value and which operations add to it.
- A deterministic order with an explicit tie-breaker.
- The cost of maintaining totals versus computing them at query time.

## Part 3 — Scheduled payments
Add operations to schedule a payment for execution at a later time and to accept a payment. Their exact parameter lists were not preserved; propose signatures in the style of Level 1, with the timestamp first.

The main difficulty is execution order in time. Scheduling a payment is not just storing a record when `schedule_payment` is called. From then on, every operation, whatever it is, may first have to execute the scheduled payments that became due before its timestamp, and only then do its own work. A balance, a transfer check or a ranking computed without that step sees stale state.

### Clarifying Questions for this Part
- What does accepting a payment mean: must the recipient accept a scheduled payment before it can execute, or does acceptance complete it in some other way? What happens to a payment that is never accepted?
- What does scheduling return, so that the payment can be referred to later (for example, when accepting it)?
- Does a payment due exactly at an operation's timestamp run before that operation?
If several payments are due, do they run in order of due time, and how are equal due times ordered?
- What happens when a payment comes due and the payer cannot cover it: is it skipped, retried later, or cancelled?

### What This Part Should Cover
- A mechanism that processes due payments before every operation, in a deterministic order.
- A data structure for pending payments and its cost per operation.
- Stated semantics for acceptance, insufficient funds and equal timestamps.

## Part 4 — Merge accounts
Add an operation that merges two accounts, retaining both accounts' balances and transaction histories.

### Clarifying Questions for this Part
- Which account id survives the merge, and can the other id be used again later?
- What happens to scheduled payments still pending for the merged-away account, as payer or as recipient?
- After a merge, does the surviving account's outgoing total for `top_spenders include the other account's history?
- Can an account be merged with itself or with an account that does not exist?

### What This Part Should Cover
- Combining balances, histories and derived totals correctly.
- Re-pointing or cancelling pending scheduled payments that reference the merged account.
- Validation, and a consistent state when a merge is rejected.

## What a Strong Answer Covers
- A data model chosen in Level 1 that survives Levels 2 to 4 without a rewrite.
- A single place where time advances and due payments run.
- Deterministic behavior: tie-breaks, execution order and return values stated up front.
- Failure paths that leave state unchanged, with tests per level that exercise them.
- The time complexity of each operation.

## Follow-up Questions
- How would you answer "what was this account's balance at timestamp T?" after scheduled payments and merges?
- If operations could arrive out of timestamp order, for example from several clients, what would break and how would you restructure the processing?
- How would you make the system safe for concurrent callers?
- If `top_spenders` is called far more often than money moves, what structure keeps it fast?
