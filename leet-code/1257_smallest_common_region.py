
def solution(regions: list[list[str]], region_1: str, region_2: str) -> str|None:
    child_parent = {}
    for reg in regions:
        for r2 in reg[1:]:
            child_parent[r2] = reg[0]

    visited = set({region1})
    current = region1
    while current:
        current = child_parent.get(current)
        if current:
            visited.add(current)

    current = region2
    while current:
        if current in visited:
            return current

        current = child_parent.get(current)

    return None



regions = [
    ("Earth","North America","South America",),
    ("North America","United States","Canada",),
    ("United States","New York","Boston",),
    ("Canada","Ontario","Quebec",),
    ("South America","Brazil",),
]
region1 = "Quebec"
region2 = "New York"

print(solution(regions, region1, region2))
