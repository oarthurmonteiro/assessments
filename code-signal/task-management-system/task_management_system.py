import itertools
from enum import StrEnum


class AssignmentStatus(StrEnum):
    ACTIVE = "active"     # not yet due, not yet completed
    COMPLETED = "completed"
    EXPIRED = "expired"   # came due without being completed


class Task:
    def __init__(self, id: str, title: str, description: str, priority: int):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority

    def update(self, title: str, description: str, priority: int) -> None:
        self.title = title
        self.description = description
        self.priority = priority

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
        }


class User:
    def __init__(self, id: str, quota: int):
        self.id = id
        self.quota = quota
        self.active_count = 0

    def has_capacity(self) -> bool:
        return self.active_count < self.quota

    def reserve_slot(self) -> None:
        self.active_count += 1

    def release_slot(self) -> None:
        self.active_count -= 1


class Assignment:
    def __init__(self, id: str, task_id: str, user_id: str, due_time: int):
        self.id = id
        self.task_id = task_id
        self.user_id = user_id
        self.due_time = due_time
        self.status = AssignmentStatus.ACTIVE


class TaskRepository:
    def __init__(self):
        self._tasks: dict[str, Task] = {}

    def exists(self, task_id: str) -> bool:
        return task_id in self._tasks

    def create(self, task_id: str, title: str, description: str, priority: int) -> bool:
        if self.exists(task_id):
            return False

        self._tasks[task_id] = Task(task_id, title, description, priority)
        return True

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())


class UserRepository:
    def __init__(self):
        self._users: dict[str, User] = {}

    def exists(self, user_id: str) -> bool:
        return user_id in self._users

    def create(self, user_id: str, quota: int) -> bool:
        if self.exists(user_id):
            return False

        self._users[user_id] = User(user_id, quota)
        return True

    def get(self, user_id: str) -> User | None:
        return self._users.get(user_id)


class AssignmentRepository:
    def __init__(self):
        self._assignments: dict[str, Assignment] = {}
        self._ids = itertools.count(1)

    def next_id(self) -> str:
        return str(next(self._ids))

    def save(self, assignment: Assignment) -> None:
        self._assignments[assignment.id] = assignment

    def get(self, assignment_id: str) -> Assignment | None:
        return self._assignments.get(assignment_id)

    def active(self) -> list[Assignment]:
        return [a for a in self._assignments.values() if a.status == AssignmentStatus.ACTIVE]

    def expired(self) -> list[Assignment]:
        return [a for a in self._assignments.values() if a.status == AssignmentStatus.EXPIRED]


class TaskManagementSystem:
    def __init__(self):
        self._tasks = TaskRepository()
        self._users = UserRepository()
        self._assignments = AssignmentRepository()

    # ------------------------------------------------------------------
    # Part 1 — Basic task operations
    # ------------------------------------------------------------------

    def add_task(self, timestamp: int, task_id: str, title: str, description: str, priority: int) -> bool:
        self._expire_due_assignments(timestamp)
        return self._tasks.create(task_id, title, description, priority)

    def update_task(self, timestamp: int, task_id: str, title: str, description: str, priority: int) -> bool:
        self._expire_due_assignments(timestamp)
        task = self._tasks.get(task_id)
        if task is None:
            return False

        task.update(title, description, priority)
        return True

    def get_task(self, timestamp: int, task_id: str) -> dict | None:
        self._expire_due_assignments(timestamp)
        task = self._tasks.get(task_id)
        return task.to_dict() if task else None

    # ------------------------------------------------------------------
    # Part 2 — Search and listing by priority
    # ------------------------------------------------------------------

    def search_tasks(self, timestamp: int, keyword: str) -> list[str]:
        self._expire_due_assignments(timestamp)
        keyword = keyword.lower()
        matches = [t for t in self._tasks.get_all() if keyword in t.title.lower()]
        matches.sort(key=lambda t: t.id)
        return [t.id for t in matches]

    def list_tasks(self, timestamp: int) -> list[str]:
        self._expire_due_assignments(timestamp)
        tasks = sorted(self._tasks.get_all(), key=lambda t: (-t.priority, t.id))
        return [t.id for t in tasks]

    # ------------------------------------------------------------------
    # Part 3 — Users, quotas and expiring assignments
    # ------------------------------------------------------------------
    #
    # A task is just a template: it carries no assignment state of its own.
    # Any number of independent assignments can be outstanding for the same
    # task at once, to the same user or to different ones. Each assignment
    # is its own record with its own due_time and status, and consumes
    # exactly one slot of the assigned user's quota for as long as it is
    # active. Completing or expiring one assignment never touches another,
    # even one for the same (task_id, user_id) pair.

    def add_user(self, timestamp: int, user_id: str, quota: int) -> bool:
        self._expire_due_assignments(timestamp)
        if quota < 0:
            return False

        return self._users.create(user_id, quota)

    def assign_task(self, timestamp: int, task_id: str, user_id: str, duration: int) -> str | None:
        self._expire_due_assignments(timestamp)
        if duration <= 0:
            return None

        task = self._tasks.get(task_id)
        user = self._users.get(user_id)
        if task is None or user is None:
            return None

        if not user.has_capacity():
            return None

        assignment = Assignment(
            self._assignments.next_id(),
            task_id, user_id,
            due_time=timestamp + duration,
        )
        self._assignments.save(assignment)
        user.reserve_slot()
        return assignment.id

    def _expire_due_assignments(self, timestamp: int) -> None:
        for assignment in self._assignments.active():
            if timestamp < assignment.due_time:
                continue

            assignment.status = AssignmentStatus.EXPIRED
            user = self._users.get(assignment.user_id)
            if user is not None:
                user.release_slot()

    # ------------------------------------------------------------------
    # Part 4 — Completing assignments and reporting overdue ones
    # ------------------------------------------------------------------

    def complete_task(self, timestamp: int, assignment_id: str, user_id: str) -> bool:
        self._expire_due_assignments(timestamp)
        assignment = self._assignments.get(assignment_id)
        if assignment is None or assignment.status != AssignmentStatus.ACTIVE:
            return False

        if assignment.user_id != user_id:
            return False

        assignment.status = AssignmentStatus.COMPLETED
        user = self._users.get(user_id)
        if user is not None:
            user.release_slot()

        return True

    def get_overdue_assignments(self, timestamp: int) -> list[tuple[str, str, str, int]]:
        self._expire_due_assignments(timestamp)
        overdue = self._assignments.expired()
        overdue.sort(key=lambda a: (a.due_time, a.id))
        return [(a.id, a.task_id, a.user_id, a.due_time) for a in overdue]
