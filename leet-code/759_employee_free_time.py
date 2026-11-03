from itertools import pairwise

schedule = [
    [ [1,2],[5,6] ],
    [ [1,3] ],
    [ [4,10] ]
]

# flatten_schedules = [[1,2],[5,6],[1,3],[4,10]]
# flatten_schedules = [[1,2],[1,3],[4,10],[5,6]]
# flatten_schedules = [[1,3],[4,10]]
holes = [[3,4]]


def solution(schedule: list[list[list[int]]]) -> list[list[int]]:
    if not schedule: return []

    flatten_schedules = [interval for employee in schedule for interval in employee]
    flatten_schedules.sort()

    merged_schedules = [flatten_schedules[0]]
    for interval in flatten_schedules[1:]:
        start, end = interval
        if start < merged_schedules[-1][1]:
            merged_schedules[-1][1] = max(end, merged_schedules[-1][1])
            continue

        merged_schedules.append(interval)

    holes = []
    for start, end in pairwise(merged_schedules):
        holes.append([start[1], end[0]])

    return holes


print(solution(schedule))
print(solution([[[1,3],[6,7]],[[2,4]],[[2,5],[9,12]]]))
# assert solution(schedule) == holes, "Solução errada"
