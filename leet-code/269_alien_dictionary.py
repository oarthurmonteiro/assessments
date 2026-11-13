# https://leetcode.ca/all/269.html


from collections import defaultdict


def solution(words: list[str]) -> str:
    graph = build_graph(words)
    visited = set()
    recursion_stack = set()

    result = []
    def dfs(node):
        visited.add(node)
        recursion_stack.add(node)

        for neighbor in graph[node]:
            if neighbor in recursion_stack:
                return ""

            if neighbor not in visited:
                dfs(neighbor)

        recursion_stack.remove(node)
        result.append(node)

    dfs(words[0][0])

    return "".join(result)


def build_graph(words: list[str]) -> dict[str, list[str]]:
    graph = defaultdict(list)
    for idx in range(len(words)-1):
        word = words[idx]
        adjacent = words[idx+1]

        min_len = min(len(word), len(adjacent))
        j = 0
        has_different = False
        while j < min_len:
            if word[j] == adjacent[j]:
                j += 1
                continue

            has_different = True
            break

        if has_different:
            graph[word[j]].append(adjacent[j])
        else:
            if j + 1 < len(adjacent):
                graph[word[j]].append(adjacent[j + 1])

    return graph

from collections import defaultdict, deque

def alienOrder(words: list[str]) -> str:
    # Step 1: Initialize the graph and in-degree count for all unique characters
    graph = defaultdict(set)
    in_degree = {char: 0 for word in words for char in word}

    # Step 2: Build the graph by comparing adjacent words
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))

        # Edge case: Check if a longer word is a prefix of a shorter word (invalid order)
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""

        # Find the first mismatching character
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in graph[w1[j]]:
                    graph[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break

    # Step 3: Push all nodes with an in-degree of 0 into the BFS queue
    queue = deque([char for char, degree in in_degree.items() if degree == 0])
    result = []

    # Step 4: Process the queue (Kahn's Algorithm)
    while queue:
        curr = queue.popleft()
        result.append(curr)

        for neighbor in graph[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Step 5: If result doesn't include all characters, a cycle exists (invalid order)
    if len(result) != len(in_degree):
        return ""

    return "".join(result)

print(build_graph([
  "wrt",
  "wrf",
  "er",
  "ett",
  "rftt"
]))

print(solution([
  "wrt",
  "wrf",
  "er",
  "ett",
  "rftt"
])) # ftrew

print(solution(["z", "x"])) # xz
print(solution(["z", "x", "z"])) # z


# "wertf"
# assert solution([
#   "wrt",
#   "wrf",
#   "er",
#   "ett",
#   "rftt"
# ]) == "wertf"
#
# assert solution(["z", "x"]) == "zx"

# assert solution(["z", "x", "z"]) == ""
