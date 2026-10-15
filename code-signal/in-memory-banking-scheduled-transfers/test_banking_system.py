"""
Tests for BankingSystem (CHALLENGE.md), organized by part.

ASSUMED INTERFACE / CONTRACT (the challenge leaves several design decisions
open on purpose; these are the choices this suite is written against —
adjust `banking_system.py` to match, or say so and I'll adjust the tests):

    create_account(timestamp: int, account_id: str) -> bool
        True if created. False if account_id already exists or on any
        invalid input. New accounts start at balance 0 with outgoing
        total 0.

    deposit(timestamp: int, account_id: str, amount: int) -> Optional[int]
        Returns the account's new balance on success. None for an
        unknown account or amount <= 0. Never counts toward outgoing
        totals (it's incoming, not a spend).

    get_balance(timestamp: int, account_id: str) -> Optional[int]
        Not part of the original interface — added because none of the
        given operations expose a way to observe a balance directly.
        None for an unknown account. Like every other operation, it
        first executes any scheduled payments whose due_time <=
        timestamp, so it always reflects up-to-date state.

    transfer(timestamp, source_id, target_id, amount) -> Optional[int]
        Returns source's new balance on success. None for: unknown
        source/target, source_id == target_id, amount <= 0, or
        insufficient funds. All-or-nothing. Counts toward source's
        outgoing total immediately (not deferred).

    top_spenders(timestamp: int, n: int) -> list[str]
        Entries formatted as "accountId(outgoingTotal)". Outgoing total
        = amounts sent via transfer() + amounts sent via scheduled
        payments that have already executed (not while merely
        scheduled). Sorted by total descending; ties broken by
        account_id ascending. If n >= number of accounts, all accounts
        are returned (including ones with outgoing total 0), same
        ordering rules.

    schedule_payment(timestamp, payer_id, recipient_id, amount, due_time) -> Optional[str]
        Recipient is fixed at scheduling time (this exact signature
        isn't given by the challenge — only that scheduling and
        accepting exist — so this is this suite's concrete proposal).
        Returns a new payment_id. None for: unknown payer/recipient,
        payer_id == recipient_id, amount <= 0, or due_time <= timestamp.
        Scheduling does NOT reserve/debit funds up front; funds are
        only checked when due_time is reached.

    accept_payment(timestamp, recipient_id, payment_id) -> bool
        Marks a pending, not-yet-due payment as accepted. True on
        success. False for: unknown payment_id, a recipient_id that
        doesn't match the payment's actual recipient, or a payment
        that already executed or already came due unaccepted (at
        which point it's expired and can never be accepted or
        executed).

    merge_accounts(timestamp, target_id, source_id) -> bool
        Folds source_id into target_id: target's balance and outgoing
        total become the sum of both. source_id no longer exists
        afterward (create_account(source_id) would succeed again as a
        brand-new account). False for: unknown target/source, or
        target_id == source_id. Any payment still pending at merge
        time where source_id was payer or recipient is re-pointed to
        target_id, rather than cancelled.

Processing model: every operation first executes any scheduled payment
whose due_time <= that operation's timestamp (ascending due_time, ties
broken by payment creation order / ascending payment_id), before doing
its own work. Timestamps are assumed non-decreasing across calls.

Run with: pytest test_banking_system.py -v
"""

import pytest

from banking_system import BankingSystem


@pytest.fixture
def bank():
    return BankingSystem()


def fund(bank, t, account_id, amount):
    """Helper: create an account and give it an opening balance via deposit."""
    bank.create_account(t, account_id)
    bank.deposit(t, account_id, amount)


# ---------------------------------------------------------------------------
# Part 1 — Basic banking operations
# ---------------------------------------------------------------------------

class TestCreateAccount:
    def test_create_new_account_returns_true(self, bank):
        assert bank.create_account(1, "alice") is True

    def test_new_account_starts_at_zero_balance(self, bank):
        bank.create_account(1, "alice")
        assert bank.get_balance(1, "alice") == 0

    def test_duplicate_create_returns_false(self, bank):
        bank.create_account(1, "alice")
        assert bank.create_account(2, "alice") is False

    def test_duplicate_create_does_not_reset_balance(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(2, "alice")
        assert bank.get_balance(2, "alice") == 100

    def test_unknown_account_balance_is_none(self, bank):
        assert bank.get_balance(1, "ghost") is None


class TestDeposit:
    def test_deposit_returns_new_balance(self, bank):
        bank.create_account(1, "alice")
        assert bank.deposit(2, "alice", 50) == 50

    def test_multiple_deposits_accumulate(self, bank):
        bank.create_account(1, "alice")
        bank.deposit(2, "alice", 50)
        assert bank.deposit(3, "alice", 25) == 75

    def test_deposit_unknown_account_fails(self, bank):
        assert bank.deposit(1, "ghost", 50) is None

    @pytest.mark.parametrize("amount", [0, -1, -100])
    def test_deposit_non_positive_amount_fails(self, bank, amount):
        bank.create_account(1, "alice")
        assert bank.deposit(2, "alice", amount) is None
        assert bank.get_balance(2, "alice") == 0

    def test_deposit_does_not_count_as_outgoing(self, bank):
        bank.create_account(1, "alice")
        bank.deposit(2, "alice", 500)
        assert bank.top_spenders(3, 1) == ["alice(0)"]


class TestTransfer:
    def test_successful_transfer_returns_sources_new_balance(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")

        assert bank.transfer(2, "alice", "bob", 40) == 60
        assert bank.get_balance(2, "alice") == 60
        assert bank.get_balance(2, "bob") == 40

    def test_transfer_exact_balance_succeeds(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")

        assert bank.transfer(2, "alice", "bob", 100) == 0
        assert bank.get_balance(2, "bob") == 100

    def test_transfer_unknown_source_fails_and_is_atomic(self, bank):
        fund(bank, 1, "bob", 10)

        assert bank.transfer(2, "ghost", "bob", 10) is None
        assert bank.get_balance(2, "bob") == 10

    def test_transfer_unknown_target_fails_and_is_atomic(self, bank):
        fund(bank, 1, "alice", 100)

        assert bank.transfer(2, "alice", "ghost", 10) is None
        assert bank.get_balance(2, "alice") == 100

    def test_transfer_to_self_fails(self, bank):
        fund(bank, 1, "alice", 100)

        assert bank.transfer(2, "alice", "alice", 10) is None
        assert bank.get_balance(2, "alice") == 100

    @pytest.mark.parametrize("amount", [0, -1, -50])
    def test_transfer_non_positive_amount_fails(self, bank, amount):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")

        assert bank.transfer(2, "alice", "bob", amount) is None
        assert bank.get_balance(2, "alice") == 100

    def test_transfer_insufficient_funds_fails_and_is_atomic(self, bank):
        fund(bank, 1, "alice", 30)
        bank.create_account(1, "bob")

        assert bank.transfer(2, "alice", "bob", 31) is None
        assert bank.get_balance(2, "alice") == 30
        assert bank.get_balance(2, "bob") == 0


# ---------------------------------------------------------------------------
# Part 2 — Top spenders
# ---------------------------------------------------------------------------

class TestTopSpenders:
    def test_no_accounts_returns_empty(self, bank):
        assert bank.top_spenders(1, 5) == []

    def test_n_zero_returns_empty(self, bank):
        fund(bank, 1, "alice", 100)
        assert bank.top_spenders(2, 0) == []

    def test_ranks_by_outgoing_total_descending(self, bank):
        fund(bank, 1, "alice", 100)
        fund(bank, 1, "bob", 100)
        bank.create_account(1, "carol")

        bank.transfer(2, "alice", "carol", 70)
        bank.transfer(2, "bob", "carol", 30)

        assert bank.top_spenders(3, 2) == ["alice(70)", "bob(30)"]

    def test_ties_broken_by_account_id_ascending(self, bank):
        fund(bank, 1, "bob", 100)
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "carol")

        bank.transfer(2, "bob", "carol", 20)
        bank.transfer(2, "alice", "carol", 20)

        assert bank.top_spenders(3, 2) == ["alice(20)", "bob(20)"]

    def test_n_greater_than_accounts_returns_all_including_zero_outgoing(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")  # no outgoing at all
        bank.transfer(2, "alice", "bob", 10)

        assert bank.top_spenders(3, 10) == ["alice(10)", "bob(0)"]

    def test_n_less_than_accounts_returns_only_top_n(self, bank):
        fund(bank, 1, "alice", 100)
        fund(bank, 1, "bob", 100)
        bank.create_account(1, "carol")

        bank.transfer(2, "alice", "carol", 50)
        bank.transfer(2, "bob", "carol", 10)

        assert bank.top_spenders(3, 1) == ["alice(50)"]

    def test_multiple_transfers_accumulate_into_total(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")

        bank.transfer(2, "alice", "bob", 10)
        bank.transfer(3, "alice", "bob", 20)

        assert bank.top_spenders(4, 1) == ["alice(30)"]

    def test_failed_transfer_does_not_affect_outgoing_total(self, bank):
        fund(bank, 1, "alice", 30)
        bank.create_account(1, "bob")

        bank.transfer(2, "alice", "bob", 31)  # insufficient funds, fails

        assert bank.top_spenders(3, 1) == ["alice(0)"]


# ---------------------------------------------------------------------------
# Part 3 — Scheduled payments
# ---------------------------------------------------------------------------

class TestSchedulePaymentValidation:
    def test_returns_a_payment_id(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")

        payment_id = bank.schedule_payment(2, "alice", "bob", 40, due_time=10)
        assert isinstance(payment_id, str)
        assert payment_id

    def test_payment_ids_are_unique(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")

        id1 = bank.schedule_payment(2, "alice", "bob", 10, due_time=10)
        id2 = bank.schedule_payment(2, "alice", "bob", 10, due_time=10)
        assert id1 != id2

    def test_scheduling_does_not_debit_payer_immediately(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")

        bank.schedule_payment(2, "alice", "bob", 40, due_time=10)
        assert bank.get_balance(2, "alice") == 100

    def test_unknown_payer_fails(self, bank):
        bank.create_account(1, "bob")
        assert bank.schedule_payment(2, "ghost", "bob", 10, due_time=10) is None

    def test_unknown_recipient_fails(self, bank):
        fund(bank, 1, "alice", 100)
        assert bank.schedule_payment(2, "alice", "ghost", 10, due_time=10) is None

    def test_self_payment_fails(self, bank):
        fund(bank, 1, "alice", 100)
        assert bank.schedule_payment(2, "alice", "alice", 10, due_time=10) is None

    @pytest.mark.parametrize("amount", [0, -1, -50])
    def test_non_positive_amount_fails(self, bank, amount):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        assert bank.schedule_payment(2, "alice", "bob", amount, due_time=10) is None

    def test_due_time_not_after_timestamp_fails(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        assert bank.schedule_payment(5, "alice", "bob", 10, due_time=5) is None
        assert bank.schedule_payment(5, "alice", "bob", 10, due_time=4) is None


class TestAcceptPayment:
    def test_accept_before_due_time_succeeds(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        payment_id = bank.schedule_payment(2, "alice", "bob", 40, due_time=10)

        assert bank.accept_payment(3, "bob", payment_id) is True

    def test_accept_unknown_payment_id_fails(self, bank):
        bank.create_account(1, "bob")
        assert bank.accept_payment(1, "bob", "no-such-id") is False

    def test_accept_with_wrong_recipient_fails(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        bank.create_account(1, "carol")
        payment_id = bank.schedule_payment(2, "alice", "bob", 40, due_time=10)

        assert bank.accept_payment(3, "carol", payment_id) is False

    def test_accept_after_due_time_has_passed_fails(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        payment_id = bank.schedule_payment(2, "alice", "bob", 40, due_time=10)

        assert bank.accept_payment(15, "bob", payment_id) is False


class TestScheduledPaymentExecution:
    def test_accepted_payment_executes_once_due_time_is_reached(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        payment_id = bank.schedule_payment(2, "alice", "bob", 40, due_time=10)
        bank.accept_payment(3, "bob", payment_id)

        assert bank.get_balance(10, "alice") == 60
        assert bank.get_balance(10, "bob") == 40

    def test_due_time_is_inclusive(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        payment_id = bank.schedule_payment(2, "alice", "bob", 40, due_time=10)
        bank.accept_payment(3, "bob", payment_id)

        # An operation stamped exactly at due_time must see the payment applied.
        assert bank.get_balance(10, "bob") == 40

    def test_unaccepted_payment_never_executes(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        bank.schedule_payment(2, "alice", "bob", 40, due_time=10)

        assert bank.get_balance(20, "alice") == 100
        assert bank.get_balance(20, "bob") == 0

    def test_insufficient_funds_at_due_time_is_skipped_permanently(self, bank):
        fund(bank, 1, "alice", 10)
        bank.create_account(1, "bob")
        payment_id = bank.schedule_payment(2, "alice", "bob", 40, due_time=10)
        bank.accept_payment(3, "bob", payment_id)

        assert bank.get_balance(10, "bob") == 0

        # Even if alice can now afford it, a skipped payment never retries.
        bank.deposit(11, "alice", 1000)
        assert bank.get_balance(12, "bob") == 0

    def test_due_payment_executes_as_a_side_effect_of_any_operation(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        bank.create_account(1, "zelda")
        payment_id = bank.schedule_payment(2, "alice", "bob", 40, due_time=10)
        bank.accept_payment(3, "bob", payment_id)

        # An unrelated operation at t=10 must trigger the sweep...
        bank.deposit(10, "zelda", 1)
        # ...so a query for alice's balance at the same timestamp already
        # reflects it, without alice/bob being touched directly at t=10.
        assert bank.get_balance(10, "alice") == 60

    def test_executed_payment_counts_toward_outgoing_total(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        payment_id = bank.schedule_payment(2, "alice", "bob", 40, due_time=10)
        bank.accept_payment(3, "bob", payment_id)

        assert bank.top_spenders(5, 1) == ["alice(0)"]  # not yet due
        assert bank.top_spenders(10, 1) == ["alice(40)"]  # executed by now

    def test_multiple_due_payments_execute_in_scheduling_order(self, bank):
        fund(bank, 1, "alice", 100)
        bank.create_account(1, "bob")
        bank.create_account(1, "carol")

        first = bank.schedule_payment(2, "alice", "bob", 60, due_time=10)
        second = bank.schedule_payment(2, "alice", "carol", 60, due_time=10)
        bank.accept_payment(3, "bob", first)
        bank.accept_payment(3, "carol", second)

        # Combined (120) exceeds alice's balance (100): the earlier-scheduled
        # payment succeeds, the later one is skipped for insufficient funds.
        assert bank.get_balance(10, "bob") == 60
        assert bank.get_balance(10, "carol") == 0
        assert bank.get_balance(10, "alice") == 40


# ---------------------------------------------------------------------------
# Part 4 — Merge accounts
# ---------------------------------------------------------------------------

class TestMergeAccounts:
    def test_unknown_target_fails(self, bank):
        bank.create_account(1, "bob")
        assert bank.merge_accounts(2, "ghost", "bob") is False

    def test_unknown_source_fails(self, bank):
        bank.create_account(1, "alice")
        assert bank.merge_accounts(2, "alice", "ghost") is False

    def test_merging_with_self_fails(self, bank):
        bank.create_account(1, "alice")
        assert bank.merge_accounts(2, "alice", "alice") is False

    def test_merge_sums_balances_into_target(self, bank):
        fund(bank, 1, "alice", 100)
        fund(bank, 1, "bob", 30)

        assert bank.merge_accounts(2, "alice", "bob") is True
        assert bank.get_balance(2, "alice") == 130

    def test_source_no_longer_exists_after_merge(self, bank):
        fund(bank, 1, "alice", 100)
        fund(bank, 1, "bob", 30)
        bank.merge_accounts(2, "alice", "bob")

        assert bank.get_balance(2, "bob") is None

    def test_source_id_can_be_reused_after_merge(self, bank):
        fund(bank, 1, "alice", 100)
        fund(bank, 1, "bob", 30)
        bank.merge_accounts(2, "alice", "bob")

        assert bank.create_account(3, "bob") is True
        assert bank.get_balance(3, "bob") == 0

    def test_outgoing_totals_combine_under_target(self, bank):
        fund(bank, 1, "alice", 100)
        fund(bank, 1, "bob", 100)
        bank.create_account(1, "carol")

        bank.transfer(2, "alice", "carol", 30)
        bank.transfer(2, "bob", "carol", 20)
        bank.merge_accounts(3, "alice", "bob")

        assert bank.top_spenders(4, 1) == ["alice(50)"]

    def test_pending_payment_with_merged_away_payer_is_repointed(self, bank):
        fund(bank, 1, "alice", 20)
        fund(bank, 1, "bob", 100)
        bank.create_account(1, "carol")

        payment_id = bank.schedule_payment(2, "bob", "carol", 60, due_time=10)
        bank.accept_payment(3, "carol", payment_id)
        bank.merge_accounts(4, "alice", "bob")  # bob (payer) merged away

        # alice now has 20 + 100 = 120, enough to cover the repointed payment.
        assert bank.get_balance(10, "carol") == 60
        assert bank.get_balance(10, "alice") == 60

    def test_pending_payment_with_merged_away_recipient_is_repointed(self, bank):
        fund(bank, 1, "alice", 100)
        fund(bank, 1, "bob", 10)
        bank.create_account(1, "carol")

        payment_id = bank.schedule_payment(2, "alice", "bob", 40, due_time=10)
        bank.merge_accounts(4, "carol", "bob")  # bob (recipient) merged away

        # Acceptance must now happen under the new recipient id.
        assert bank.accept_payment(5, "carol", payment_id) is True
        assert bank.get_balance(10, "carol") == 50  # 10 (bob's) + 40
        assert bank.get_balance(10, "alice") == 60
