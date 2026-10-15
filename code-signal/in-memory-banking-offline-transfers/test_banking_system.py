"""
Tests for BankingSystem (CHALLENGE.md), organized by part.

ASSUMED INTERFACE / CONTRACT (the challenge's clarifying questions are
intentionally open-ended; these are the choices these tests are written
against — adjust `banking_system.py` to match, or tell me to change the
tests if your assessment used different names/semantics):

    create_user(user_id: str) -> bool
        True if created. False if user_id already exists. New users
        start with a balance of 0.

    deposit(user_id: str, amount: int) -> bool
        Only way money enters the system (not in the illustrative
        interface, added because create_user takes no balance).
        True on success. False for unknown user or amount <= 0.

    get_balance(user_id: str) -> Optional[int]
        Spendable balance: raw deposits/transfers in, minus amounts
        already reserved by this user's own pending offline transfers.
        None for an unknown user.

    transfer(from_id: str, to_id: str, amount: int) -> bool
        Immediate, all-or-nothing. True on success. False for: unknown
        from_id/to_id, from_id == to_id, amount <= 0, or insufficient
        spendable balance. Balances must not change on failure.

    offline_transfer(from_id: str, to_id: str, amount: int) -> Optional[str]
        Returns a new, unique transfer_id string on success; None on
        the same failure conditions as transfer(). The amount is
        reserved out of the sender's spendable balance immediately
        (get_balance(from_id) drops right away); the recipient is not
        credited until the transfer is processed.

    process_offline_transfers() -> None
        Applies every currently pending offline transfer, in the
        deterministic order they were created (FIFO), crediting each
        recipient. No-op when nothing is pending.

    delete_transfer(transfer_id: str) -> bool
        Only a transfer that is still pending (not yet processed, not
        already deleted) can be deleted. True on success, restoring the
        reserved amount to the sender's spendable balance and
        permanently preventing that transfer from ever taking effect
        (a later process_offline_transfers() must skip it). False for
        an unknown transfer_id or one that is no longer pending
        (already processed or already deleted) — completed transfers
        are not reversed.

Run with: pytest test_banking_system.py -v
"""

import pytest

from banking_system import BankingSystem


@pytest.fixture
def bank():
    return BankingSystem()


def fund(bank, user_id, amount):
    """Helper: create a user and give it an opening balance via deposit."""
    bank.create_user(user_id)
    bank.deposit(user_id, amount)


# ---------------------------------------------------------------------------
# Part 1 — Users and immediate transfers
# ---------------------------------------------------------------------------

class TestCreateUser:
    def test_create_new_user_returns_true(self, bank):
        assert bank.create_user("alice") is True

    def test_new_user_starts_at_zero_balance(self, bank):
        bank.create_user("alice")
        assert bank.get_balance("alice") == 0

    def test_duplicate_create_returns_false(self, bank):
        bank.create_user("alice")
        assert bank.create_user("alice") is False

    def test_duplicate_create_does_not_reset_balance(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("alice")
        assert bank.get_balance("alice") == 100

    def test_unknown_user_balance_is_none(self, bank):
        assert bank.get_balance("ghost") is None


class TestDeposit:
    def test_deposit_increases_balance(self, bank):
        bank.create_user("alice")
        assert bank.deposit("alice", 50) is True
        assert bank.get_balance("alice") == 50

    def test_multiple_deposits_accumulate(self, bank):
        bank.create_user("alice")
        bank.deposit("alice", 50)
        bank.deposit("alice", 25)
        assert bank.get_balance("alice") == 75

    def test_deposit_unknown_user_fails(self, bank):
        assert bank.deposit("ghost", 50) is False

    @pytest.mark.parametrize("amount", [0, -1, -100])
    def test_deposit_non_positive_amount_fails(self, bank, amount):
        bank.create_user("alice")
        assert bank.deposit("alice", amount) is False
        assert bank.get_balance("alice") == 0


class TestImmediateTransfer:
    def test_successful_transfer_moves_funds(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")

        assert bank.transfer("alice", "bob", 40) is True
        assert bank.get_balance("alice") == 60
        assert bank.get_balance("bob") == 40

    def test_transfer_exact_balance_succeeds(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")

        assert bank.transfer("alice", "bob", 100) is True
        assert bank.get_balance("alice") == 0
        assert bank.get_balance("bob") == 100

    def test_transfer_unknown_sender_fails_and_is_atomic(self, bank):
        bank.create_user("bob")
        bank.deposit("bob", 10)

        assert bank.transfer("ghost", "bob", 10) is False
        assert bank.get_balance("bob") == 10

    def test_transfer_unknown_recipient_fails_and_is_atomic(self, bank):
        fund(bank, "alice", 100)

        assert bank.transfer("alice", "ghost", 10) is False
        assert bank.get_balance("alice") == 100

    def test_transfer_to_self_fails(self, bank):
        fund(bank, "alice", 100)

        assert bank.transfer("alice", "alice", 10) is False
        assert bank.get_balance("alice") == 100

    @pytest.mark.parametrize("amount", [0, -1, -50])
    def test_transfer_non_positive_amount_fails(self, bank, amount):
        fund(bank, "alice", 100)
        bank.create_user("bob")

        assert bank.transfer("alice", "bob", amount) is False
        assert bank.get_balance("alice") == 100
        assert bank.get_balance("bob") == 0

    def test_transfer_insufficient_funds_fails_and_is_atomic(self, bank):
        fund(bank, "alice", 30)
        bank.create_user("bob")

        assert bank.transfer("alice", "bob", 31) is False
        assert bank.get_balance("alice") == 30
        assert bank.get_balance("bob") == 0


# ---------------------------------------------------------------------------
# Part 2 — Offline transfers
# ---------------------------------------------------------------------------

class TestOfflineTransferCreation:
    def test_returns_a_transfer_id(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")

        transfer_id = bank.offline_transfer("alice", "bob", 40)
        assert isinstance(transfer_id, str)
        assert transfer_id

    def test_transfer_ids_are_unique(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")

        id1 = bank.offline_transfer("alice", "bob", 10)
        id2 = bank.offline_transfer("alice", "bob", 10)
        assert id1 != id2

    def test_reserves_senders_spendable_balance_immediately(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")

        bank.offline_transfer("alice", "bob", 40)
        assert bank.get_balance("alice") == 60

    def test_recipient_not_credited_before_processing(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")

        bank.offline_transfer("alice", "bob", 40)
        assert bank.get_balance("bob") == 0

    def test_unknown_sender_fails(self, bank):
        bank.create_user("bob")
        assert bank.offline_transfer("ghost", "bob", 10) is None

    def test_unknown_recipient_fails_and_reserves_nothing(self, bank):
        fund(bank, "alice", 100)
        assert bank.offline_transfer("alice", "ghost", 10) is None
        assert bank.get_balance("alice") == 100

    def test_to_self_fails(self, bank):
        fund(bank, "alice", 100)
        assert bank.offline_transfer("alice", "alice", 10) is None
        assert bank.get_balance("alice") == 100

    @pytest.mark.parametrize("amount", [0, -1, -50])
    def test_non_positive_amount_fails(self, bank, amount):
        fund(bank, "alice", 100)
        bank.create_user("bob")

        assert bank.offline_transfer("alice", "bob", amount) is None
        assert bank.get_balance("alice") == 100

    def test_insufficient_spendable_balance_fails(self, bank):
        fund(bank, "alice", 30)
        bank.create_user("bob")

        assert bank.offline_transfer("alice", "bob", 31) is None
        assert bank.get_balance("alice") == 30

    def test_second_offline_transfer_respects_prior_reservation(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")

        assert bank.offline_transfer("alice", "bob", 80) is not None
        # Only 20 left spendable now, so a second 30 transfer must fail.
        assert bank.offline_transfer("alice", "bob", 30) is None
        assert bank.get_balance("alice") == 20

    def test_interaction_with_immediate_transfer(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")

        bank.offline_transfer("alice", "bob", 80)
        # Only 20 spendable remains; an immediate transfer of 21 must fail.
        assert bank.transfer("alice", "bob", 21) is False
        assert bank.transfer("alice", "bob", 20) is True
        assert bank.get_balance("alice") == 0


class TestOfflineTransferProcessing:
    def test_process_credits_recipient_and_keeps_sender_reduced(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")
        bank.offline_transfer("alice", "bob", 40)

        bank.process_offline_transfers()

        assert bank.get_balance("alice") == 60
        assert bank.get_balance("bob") == 40

    def test_process_applies_all_pending_in_one_call(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")
        bank.create_user("carol")
        bank.offline_transfer("alice", "bob", 30)
        bank.offline_transfer("alice", "carol", 20)

        bank.process_offline_transfers()

        assert bank.get_balance("alice") == 50
        assert bank.get_balance("bob") == 30
        assert bank.get_balance("carol") == 20

    def test_process_with_nothing_pending_is_a_no_op(self, bank):
        fund(bank, "alice", 100)
        bank.process_offline_transfers()
        assert bank.get_balance("alice") == 100

    def test_process_is_idempotent_for_already_applied_transfers(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")
        bank.offline_transfer("alice", "bob", 40)

        bank.process_offline_transfers()
        bank.process_offline_transfers()  # must not double-credit bob

        assert bank.get_balance("alice") == 60
        assert bank.get_balance("bob") == 40

    def test_no_money_created_or_lost_across_mixed_operations(self, bank):
        fund(bank, "alice", 100)
        fund(bank, "bob", 50)
        bank.create_user("carol")
        total = 150

        bank.transfer("alice", "bob", 20)
        bank.offline_transfer("bob", "carol", 15)
        bank.offline_transfer("alice", "carol", 10)
        bank.process_offline_transfers()
        bank.transfer("carol", "alice", 5)

        reconciled = (
            bank.get_balance("alice")
            + bank.get_balance("bob")
            + bank.get_balance("carol")
        )
        assert reconciled == total


# ---------------------------------------------------------------------------
# Part 3 — Deleting a transfer
# ---------------------------------------------------------------------------

class TestDeleteTransfer:
    def test_delete_pending_transfer_returns_true(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")
        transfer_id = bank.offline_transfer("alice", "bob", 40)

        assert bank.delete_transfer(transfer_id) is True

    def test_delete_restores_senders_spendable_balance(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")
        transfer_id = bank.offline_transfer("alice", "bob", 40)
        assert bank.get_balance("alice") == 60

        bank.delete_transfer(transfer_id)
        assert bank.get_balance("alice") == 100

    def test_deleted_transfer_never_takes_effect(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")
        transfer_id = bank.offline_transfer("alice", "bob", 40)

        bank.delete_transfer(transfer_id)
        bank.process_offline_transfers()

        assert bank.get_balance("alice") == 100
        assert bank.get_balance("bob") == 0

    def test_delete_unknown_transfer_id_fails(self, bank):
        assert bank.delete_transfer("no-such-id") is False

    def test_delete_already_processed_transfer_fails_and_does_not_reverse(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")
        transfer_id = bank.offline_transfer("alice", "bob", 40)
        bank.process_offline_transfers()

        assert bank.delete_transfer(transfer_id) is False
        assert bank.get_balance("alice") == 60
        assert bank.get_balance("bob") == 40

    def test_delete_is_exactly_once(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")
        transfer_id = bank.offline_transfer("alice", "bob", 40)

        assert bank.delete_transfer(transfer_id) is True
        assert bank.delete_transfer(transfer_id) is False
        assert bank.get_balance("alice") == 100

    def test_deleting_one_transfer_does_not_affect_others(self, bank):
        fund(bank, "alice", 100)
        bank.create_user("bob")
        bank.create_user("carol")
        id_to_bob = bank.offline_transfer("alice", "bob", 30)
        id_to_carol = bank.offline_transfer("alice", "carol", 20)

        bank.delete_transfer(id_to_bob)
        bank.process_offline_transfers()

        # 100 - 30 (reserved for bob) - 20 (reserved for carol) + 30 (restored on delete)
        assert bank.get_balance("alice") == 80
        assert bank.get_balance("bob") == 0
        assert bank.get_balance("carol") == 20
