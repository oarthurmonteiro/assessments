"""
Tests for TaskManagementSystem (CHALLENGE.md), organized by part.

ASSUMED INTERFACE / CONTRACT (the challenge leaves several design decisions
open on purpose; these are the choices this suite is written against —
adjust `task_management_system.py` to match, or say so and I'll adjust the
tests):

    add_task(timestamp, task_id, title, description, priority) -> bool
        True if created. False if task_id already exists.

    update_task(timestamp, task_id, title, description, priority) -> bool
        Full overwrite of all three fields. False for an unknown task_id.

    get_task(timestamp, task_id) -> Optional[dict]
        None for an unknown task_id. Otherwise a dict with id, title,
        description and priority. A task carries no assignment state of
        its own -- see assign_task below. Like every other operation, it
        first expires any assignment whose due_time <= timestamp.

    search_tasks(timestamp, keyword) -> list[str]
        Task ids whose title contains keyword, case-insensitive substring
        match. Sorted by task_id ascending.

    list_tasks(timestamp) -> list[str]
        All task ids, sorted by priority descending; ties broken by
        task_id ascending.

    add_user(timestamp, user_id, quota) -> bool
        True if created. False if user_id already exists or quota < 0.

    assign_task(timestamp, task_id, user_id, duration) -> Optional[str]
        Creates a new, independent assignment due at timestamp + duration
        and returns its id. A task can have any number of outstanding
        assignments at once, to the same user or to different users --
        there is no "already assigned" rejection. Returns None for:
        unknown task/user, a user already at quota, or duration <= 0.
        Each assignment consumes exactly one slot of its user's quota
        until it is completed or expires; other assignments (even for the
        same task/user pair) are unaffected.

    complete_task(timestamp, assignment_id, user_id) -> bool
        True if assignment_id is active and belongs to user_id, which is
        then marked completed and frees its quota slot. False for an
        unknown assignment, one already completed/expired, or one that
        belongs to a different user. An assignment that expired by this
        timestamp (even if due exactly at timestamp) can no longer be
        completed -- the expiry sweep runs first. Other assignments are
        never affected by completing this one.

    get_overdue_assignments(timestamp) -> list[tuple[str, str, str, int]]
        (assignment_id, task_id, user_id, due_time) for every assignment
        that came due without being completed, sorted by due_time
        ascending then assignment_id ascending. Entries persist as
        history once reported.

Processing model: every operation first expires any active assignment
whose due_time <= that operation's timestamp (due_time is inclusive),
before doing its own work. Expiring an assignment only frees that
assignment's slot in its user's quota -- it never touches any other
assignment. Timestamps are assumed non-decreasing across calls.

Run with: pytest test_task_management_system.py -v
"""

import pytest

from task_management_system import TaskManagementSystem


@pytest.fixture
def tms():
    return TaskManagementSystem()


# ---------------------------------------------------------------------------
# Part 1 — Basic task operations
# ---------------------------------------------------------------------------

class TestAddTask:
    def test_add_new_task_returns_true(self, tms):
        assert tms.add_task(1, "t1", "Write report", "quarterly numbers", 5) is True

    def test_duplicate_task_id_returns_false(self, tms):
        tms.add_task(1, "t1", "Write report", "desc", 5)
        assert tms.add_task(2, "t1", "Other title", "other desc", 1) is False

    def test_duplicate_add_does_not_overwrite(self, tms):
        tms.add_task(1, "t1", "Write report", "desc", 5)
        tms.add_task(2, "t1", "Other title", "other desc", 1)
        assert tms.get_task(2, "t1")["title"] == "Write report"

    def test_unknown_task_get_is_none(self, tms):
        assert tms.get_task(1, "ghost") is None


class TestUpdateTask:
    def test_update_overwrites_fields(self, tms):
        tms.add_task(1, "t1", "Draft", "v1", 1)
        assert tms.update_task(2, "t1", "Final", "v2", 5) is True

        task = tms.get_task(2, "t1")
        assert task["title"] == "Final"
        assert task["description"] == "v2"
        assert task["priority"] == 5

    def test_update_unknown_task_fails(self, tms):
        assert tms.update_task(1, "ghost", "Final", "v2", 5) is False


# ---------------------------------------------------------------------------
# Part 2 — Search and listing by priority
# ---------------------------------------------------------------------------

class TestSearchTasks:
    def test_substring_match_is_case_insensitive(self, tms):
        tms.add_task(1, "t1", "Write Report", "desc", 1)
        tms.add_task(1, "t2", "Review PR", "desc", 1)

        assert tms.search_tasks(2, "report") == ["t1"]

    def test_no_match_returns_empty(self, tms):
        tms.add_task(1, "t1", "Write Report", "desc", 1)
        assert tms.search_tasks(2, "deploy") == []

    def test_multiple_matches_sorted_by_task_id(self, tms):
        tms.add_task(1, "t2", "Report v2", "desc", 1)
        tms.add_task(1, "t1", "Report v1", "desc", 1)

        assert tms.search_tasks(2, "report") == ["t1", "t2"]


class TestListTasks:
    def test_sorted_by_priority_descending(self, tms):
        tms.add_task(1, "low", "Low", "desc", 1)
        tms.add_task(1, "high", "High", "desc", 9)
        tms.add_task(1, "mid", "Mid", "desc", 5)

        assert tms.list_tasks(2) == ["high", "mid", "low"]

    def test_ties_broken_by_task_id_ascending(self, tms):
        tms.add_task(1, "b", "B", "desc", 3)
        tms.add_task(1, "a", "A", "desc", 3)

        assert tms.list_tasks(2) == ["a", "b"]

    def test_no_tasks_returns_empty(self, tms):
        assert tms.list_tasks(1) == []


# ---------------------------------------------------------------------------
# Part 3 — Users, quotas and expiring assignments
# ---------------------------------------------------------------------------

class TestAddUser:
    def test_add_new_user_returns_true(self, tms):
        assert tms.add_user(1, "alice", 2) is True

    def test_duplicate_user_returns_false(self, tms):
        tms.add_user(1, "alice", 2)
        assert tms.add_user(2, "alice", 5) is False

    def test_negative_quota_fails(self, tms):
        assert tms.add_user(1, "alice", -1) is False


class TestAssignTask:
    def test_successful_assignment_returns_an_id(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 2)

        assignment_id = tms.assign_task(2, "t1", "alice", duration=10)
        assert isinstance(assignment_id, str)
        assert assignment_id

    def test_unknown_task_fails(self, tms):
        tms.add_user(1, "alice", 2)
        assert tms.assign_task(2, "ghost", "alice", duration=10) is None

    def test_unknown_user_fails(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        assert tms.assign_task(2, "t1", "ghost", duration=10) is None

    @pytest.mark.parametrize("duration", [0, -1, -5])
    def test_non_positive_duration_fails(self, tms, duration):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 2)

        assert tms.assign_task(2, "t1", "alice", duration=duration) is None

    def test_same_task_can_be_assigned_to_two_different_users(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        tms.add_user(1, "bob", 1)

        first = tms.assign_task(2, "t1", "alice", duration=10)
        second = tms.assign_task(2, "t1", "bob", duration=10)

        assert first is not None
        assert second is not None
        assert first != second

    def test_same_task_can_be_assigned_twice_to_the_same_user(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 2)

        first = tms.assign_task(2, "t1", "alice", duration=10)
        second = tms.assign_task(2, "t1", "alice", duration=20)

        assert first is not None
        assert second is not None
        assert first != second

    def test_each_assignment_consumes_one_quota_slot(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_task(1, "t2", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)

        assert tms.assign_task(2, "t1", "alice", duration=10) is not None
        assert tms.assign_task(2, "t2", "alice", duration=10) is None  # quota exhausted

    def test_quota_exceeded_by_repeated_assignment_to_same_task(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)

        assert tms.assign_task(2, "t1", "alice", duration=10) is not None
        assert tms.assign_task(2, "t1", "alice", duration=10) is None  # still the same user's quota


class TestAssignmentExpiry:
    def test_assignment_expires_at_due_time(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        assignment_id = tms.assign_task(2, "t1", "alice", duration=8)  # due_time = 10

        assert tms.get_overdue_assignments(10) == [(assignment_id, "t1", "alice", 10)]

    def test_expiry_frees_quota_slot(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_task(1, "t2", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        tms.assign_task(2, "t1", "alice", duration=8)  # due_time = 10

        assert tms.assign_task(10, "t2", "alice", duration=10) is not None

    def test_expiry_is_a_side_effect_of_any_operation(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_task(1, "t2", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        tms.assign_task(2, "t1", "alice", duration=8)  # due_time = 10

        tms.add_task(10, "unrelated", "Other", "desc", 1)
        assert tms.assign_task(10, "t2", "alice", duration=10) is not None

    def test_not_yet_due_assignment_stays_active(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        tms.assign_task(2, "t1", "alice", duration=8)  # due_time = 10

        assert tms.get_overdue_assignments(9) == []

    def test_expiring_one_assignment_leaves_sibling_assignment_untouched(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 2)
        early = tms.assign_task(2, "t1", "alice", duration=5)   # due_time = 7
        late = tms.assign_task(2, "t1", "alice", duration=50)   # due_time = 52

        assert tms.get_overdue_assignments(7) == [(early, "t1", "alice", 7)]
        assert tms.complete_task(8, late, "alice") is True


# ---------------------------------------------------------------------------
# Part 4 — Completing assignments and reporting overdue ones
# ---------------------------------------------------------------------------

class TestCompleteTask:
    def test_completing_active_assignment_succeeds(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        assignment_id = tms.assign_task(2, "t1", "alice", duration=10)

        assert tms.complete_task(5, assignment_id, "alice") is True

    def test_completing_frees_quota_slot(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_task(1, "t2", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        assignment_id = tms.assign_task(2, "t1", "alice", duration=10)
        tms.complete_task(5, assignment_id, "alice")

        assert tms.assign_task(5, "t2", "alice", duration=10) is not None

    def test_wrong_user_fails(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        tms.add_user(1, "bob", 1)
        assignment_id = tms.assign_task(2, "t1", "alice", duration=10)

        assert tms.complete_task(5, assignment_id, "bob") is False

    def test_unknown_assignment_fails(self, tms):
        tms.add_user(1, "alice", 1)
        assert tms.complete_task(5, "no-such-id", "alice") is False

    def test_already_expired_assignment_cannot_be_completed(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        assignment_id = tms.assign_task(2, "t1", "alice", duration=8)  # due_time = 10

        assert tms.complete_task(10, assignment_id, "alice") is False

    def test_completing_one_assignment_does_not_complete_a_sibling(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 2)
        first = tms.assign_task(2, "t1", "alice", duration=10)
        second = tms.assign_task(2, "t1", "alice", duration=10)

        assert tms.complete_task(5, first, "alice") is True
        assert tms.complete_task(5, second, "alice") is True  # still independently active

    def test_completed_assignment_is_not_reported_overdue(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        assignment_id = tms.assign_task(2, "t1", "alice", duration=8)  # due_time = 10
        tms.complete_task(5, assignment_id, "alice")

        assert tms.get_overdue_assignments(10) == []


class TestOverdueAssignments:
    def test_no_assignments_returns_empty(self, tms):
        assert tms.get_overdue_assignments(1) == []

    def test_not_yet_due_assignment_is_not_reported(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        tms.assign_task(2, "t1", "alice", duration=8)  # due_time = 10

        assert tms.get_overdue_assignments(9) == []

    def test_sorted_by_due_time_then_assignment_id(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 2)
        first = tms.assign_task(2, "t1", "alice", duration=5)   # due_time = 7
        second = tms.assign_task(2, "t1", "alice", duration=5)  # due_time = 7

        assert tms.get_overdue_assignments(7) == [
            (first, "t1", "alice", 7),
            (second, "t1", "alice", 7),
        ]

    def test_overdue_entry_persists_as_history(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        assignment_id = tms.assign_task(2, "t1", "alice", duration=8)  # due_time = 10

        tms.get_overdue_assignments(10)
        assert tms.get_overdue_assignments(50) == [(assignment_id, "t1", "alice", 10)]

    def test_multiple_users_on_same_task_reported_independently(self, tms):
        tms.add_task(1, "t1", "Title", "desc", 1)
        tms.add_user(1, "alice", 1)
        tms.add_user(1, "bob", 1)
        alice_assignment = tms.assign_task(2, "t1", "alice", duration=5)  # due_time = 7
        bob_assignment = tms.assign_task(2, "t1", "bob", duration=5)      # due_time = 7
        tms.complete_task(6, bob_assignment, "bob")

        assert tms.get_overdue_assignments(7) == [(alice_assignment, "t1", "alice", 7)]
