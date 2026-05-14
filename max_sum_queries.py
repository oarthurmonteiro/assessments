def solution(arr, queries):
    n = len(arr)
    
    P = [0] * (n + 1)
    for i in range(n):
        P[i + 1] = P[i] + arr[i]
        
    print(f"ARR: {arr}")
    print(f"P {P}")
        
    m = n + 1
    k = m.bit_length()
    sparse_table = [[0] * k for _ in range(m)]
    
    for i in range(m):
        sparse_table[i][0] = P[i]
        
    for j in range(1, k):
        for i in range(m - (1 << j) + 1):
            sparse_table[i][j] = max(sparse_table[i][j - 1], sparse_table[i + (1 << (j - 1))][j-1])
            print(f"max([{i}][{j-1}], [{i + (1 << (j - 1))}][{j-1}])")
            print(f"Sparse Table: [{i}][{j}] {sparse_table}")
            
    
    results = []
    for l, r in queries:
        length = (r + 1) - (l + 1) + 1
        j = length.bit_length() - 1
        v = max(sparse_table[l + 1][j], sparse_table[(r + 1) - (1 << j) + 1][j])
        results.append(v - P[l])
        
    return results


import unittest
import timeout_decorator

class UnitTests(unittest.TestCase):
    def test_01(self):
        arr = [1, -2, 3, 4, -1, 2, 1, -5, 4]
        queries = [(0, 3), (1, 2), (3, 4), (0, 2), (2, 4)]
        expected_result = [6, 1, 4, 2, 7]
        result = solution(arr, queries)
        self.assertEqual(result, expected_result)

    # def test_02(self):
    #     arr = [-1, -2, -3, -4, -5]
    #     queries = [(0, 1), (1, 2), (2, 3), (3, 4)]
    #     expected_result = [-1, -2, -3, -4]
    #     result = solution(arr, queries)
    #     self.assertEqual(result, expected_result)

    # def test_03(self):
    #     arr = [1, 2, 3, 4, 5]
    #     queries = [(0, 1), (1, 2), (2, 3), (3, 4)]
    #     expected_result = [3, 5, 7, 9]
    #     result = solution(arr, queries)
    #     self.assertEqual(result, expected_result)

    # def test_04(self):
    #     arr = [-90, 78, -53, 1, -69, -48, -61, 54, -6, -82, -43, -81, 3, 67, -14, -24, -96, 42, -72, 29]
    #     queries = [(6, 12), (4, 11), (7, 14), (4, 17), (12, 15)]
    #     expected_result = [-7, -69, 54, -69, 70]
    #     result = solution(arr, queries)
    #     self.assertEqual(result, expected_result)

    # def test_05(self):
    #     arr = [-72, 29, -35, -88, -95, 69, -93, -16, 52, -40, -52, -2, -6, -28, 24, 41, 71, 62, 70, 23, 3, -72, 7, -15, 24, 42, -13, -64, 3, 65, 44, -43, 97, 53, -46, 73, -87, 7, 6, -38, -72, -16, -5, -20, -1, 49, -96, -68, -22, 82]
    #     queries = [(30, 42), (42, 45), (11, 26), (26, 32), (10, 34), (27, 48), (4, 22)]
    #     expected_result = [178, 23, 258, 89, 334, 182, 83]
    #     result = solution(arr, queries)
    #     self.assertEqual(result, expected_result)

    # def test_06(self):
    #     arr = [100]
    #     queries = [(0, 0)]
    #     expected_result = [100]
    #     result = solution(arr, queries)
    #     self.assertEqual(result, expected_result)

    # def test_07(self):
    #     arr = [-25, 92, 61, -82, 88, 80, -49, -43, 39, -30, -22, -77, -24, 11, -80, 22, 62, -57, 72, 3, -75, -80, 58, -44, -33, -14, -32, -54, 49, -29, 82, 51, 97, -25, 88, 84, 31, 79, -11, -79, 62, -21, -43, -93, -62, -6, 25, -16, 13, -51, 29, -85, -14, 37, 49, -87, -45, 28, -97, 84, -47, 79, 100, 63, -80, 99, -33, -10, 63, 93, -46, 100, -78, 28, -37, 89, -44, -74, -43, 40, 39, -97, 24, -81, -2, 73, 62, -52, -89, 51, -99, 43, -66, 28, -38, -95, 84, 31, 11, -7]
    #     queries = [(22, 90), (61, 92), (14, 78), (27, 95), (84, 94), (82, 94), (60, 79), (10, 76), (5, 72), (26, 78)]
    #     expected_result = [388, 430, 255, 453, 133, 76, 383, 143, 140, 421]
    #     result = solution(arr, queries)
    #     self.assertEqual(result, expected_result)

    # @timeout_decorator.timeout(2)
    # def test_08(self):
    #     arr = list(range(1, 1001))
    #     queries = [(i, j) for i in range(1000) for j in range(i, 1000)]
    #     expected_result = [(i + j + 2) * (j - i + 1) // 2 for (i, j) in queries]
    #     result = solution(arr, queries)
    #     self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()

# result=$(python3 -m unittest discover -s .  -p '*.py' 2>&1)
# echo "${result}"