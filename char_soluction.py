def solution(S, Q):
    char_positions = {}
    for idx, char in enumerate(S):
        char_positions[char] = char_positions.get(char, [])
        char_positions[char].append(idx)
        
    n = len(S)
    results = []
    
    for c1, c2 in Q:
        p1 = char_positions.get(c1, [])
        p2 = char_positions.get(c2, [])
        
        combined = merge_sort(p1 + p2) if c1 != c2 else p1
        
        if not combined:
            results.append(n)
            continue
            
        barriers = [-1] + combined + [n]
        max_len = 0
        
        for i in range(len(barriers) - 1):
            max_len = max(max_len, barriers[i + 1] - barriers[i] - 1)
            
        results.append(max_len)
        
    return results


def merge_sort(p1, p2):
    if len(p1) > len(p2):
        p1,p2=p2,p1
        
    i,j = 0,0
    merged = []
    while i < len(p1) and j < len(p2):
        if p1[i] > p2[j]:
            merged.append(p2[j])
            j += 1
        else:
            merged.append(p1[i])
            i += 1
            
    for k in range(i, len(p1)):
        merged.append(p1[k])
        
    for k in range(j, len(p2)):
        merged.append(p2[k])
        
    return merged