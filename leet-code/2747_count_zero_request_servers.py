
def count_servers(n: int, logs: list[list[int]], x: int, queries: list[int]) -> list[int]:
    sorted_queries = sorted([(q, idx) for idx, q in enumerate(queries)])
    logs.sort(key=lambda x: x[1])

    result = [0] * len(queries)
    servers = [0] * (n + 1)
    active_servers = 0

    i = 0
    j = 0
    num_logs = len(logs)

    for q, idx in sorted_queries:
        while j < num_logs and logs[j][1] <= q:
            if servers[logs[j][0]] == 0:
                active_servers += 1

            servers[logs[j][0]] += 1
            j += 1

        while i < num_logs and logs[i][1] < q - x:
            servers[logs[i][0]] -=1
            if servers[logs[i][0]] == 0:
                active_servers -= 1

            i += 1

        result[idx] = n - active_servers

    return result



print(count_servers(
    4,
    [[2,30],[2,5],[3,9],[4,21]],
    9,
    [11,28,16,18]
))
