def solution(operations):
    
    items = {}
    size = 0
    res = []
    current_max = float('-inf')
    
    for op in operations:
        
        print(f"{op} {items}")
        
        if op[0] == 0:
            arg = op[1]
            if arg not in items:
                items[arg] = current_max
                current_max = max(current_max, arg)
                size += 1
                
            res.append(size)
            
        elif op[0] == 1:
            arg = op[1]
            if current_max == arg:
                current_max = items[arg]
                
            del items[arg]
            size -= 1
            res.append(size)
            
        elif op[0] == 2:
            if size > 0:
                res.append(current_max)
            else:
                res.append(-1)
            
    return res


operations = [[0, -67], [2], [2], [1, -67], [0, -7], [0, 90], [1, -7], [0, 64], [2], [1, 90], [0, 99], [1, 99], [2], [2], [0, 36], [2], [2], [2], [0, 100], [1, 36], [1, 100], [1, 64], [0, -36], [1, -36], [2], [0, -42], [0, 53], [2], [1, 53], [0, 90], [1, -42], [2], [2], [0, -79], [1, 90], [2], [2], [0, -45], [1, -79], [1, -45], [2], [0, 11], [2], [1, 11], [2], [0, 88], [1, 88], [2], [2], [2]]
expected_result = [1, -67, -67, 0, 1, 2, 1, 2, 90, 1, 2, 1, 64, 64, 2, 64, 64, 64, 3, 2, 1, 0, 1, 0, -1, 1, 2, 53, 1, 2, 1, 90, 90, 2, 1, -79, -79, 2, 1, 0, -1, 1, 11, 0, -1, 1, 0, -1, -1, -1]
result          = [1, -67, -67, 0, 1, 2, 1, 2, 90, 1, 2, 1, -7, -7, 2, 36, 36, 36, 3, 2, 1, 0, 1, 0, -1, 1, 2, 53, 1, 2, 1, 90, 90, 2, 1, 36, 36, 2, 1, 0, -1, 1, 36, 0, -1, 1, 0, -1, -1, -1]
print(solution(operations))