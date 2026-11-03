from itertools import pairwise


def solution(meetings_times: list[list[int]]) -> bool:
    meetings_times.sort()
    for a, b in pairwise(meetings_times):
        if b[0] < a[1]:
            return False

    return True


print(solution([[0,30],[5,10],[15,20]]))
print(solution([[7,10],[2,4]]))
