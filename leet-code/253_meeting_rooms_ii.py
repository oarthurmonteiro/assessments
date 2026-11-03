meetings = [[0, 30],[5, 10],[15, 20]]

# starts = [0,5,15]
# ends = [10,20,30]

def solution(meetings) -> int:
    starts = []
    ends = []
    for start, end in meetings:
        starts.append(start)
        ends.append(end)

    starts.sort()
    ends.sort()

    size = len(meetings)
    i, j = 0, 0
    rooms, max_rooms = 0, 0
    while i < size and j < size:
        start = starts[i]
        end = ends[j]

        if start < end:
            rooms += 1
            i += 1
        else:
            rooms -= 1
            j += 1

        max_rooms = max(max_rooms, rooms)

    return max_rooms


print(solution([[0, 30],[5, 10],[15, 20]]))
print(solution([[7,10],[2,4]]))
