import unittest


def solution(arr):
    count_numbers = {}
    for i in arr:
        count_numbers[i] = count_numbers.get(i, 0) + 1
        
    pairs = 0
    
    # S= n * (n-1) / 2
    for i in count_numbers.values():
        if i > 1:
            pairs += (i * (i-1)) / 2
            
    return pairs
    
    # [x,x] = 1 par
    # [x,x,x] = 3 par
    # [x,x,x,x] = 6 par
    # [x,x,x,x,x] = 10 par
    # [x,x,x,x,x,x] = 
    


class UnitTests(unittest.TestCase):
    def test_01(self):
        arr = [1, 1, 2, 3, 2]
        expected_result = 2
        result = solution(arr)
        self.assertEqual(result, expected_result)

    def test_02(self):
        arr = [-29, 91, 92, 40, 71, 89, -75, 61, 68, -27, -73, -95, 19, 3, 63, 79, 76, -18, 22, -38, -86, -44, -56, -67, 77, 64, -84, 71, 62, 21, 68, -80, 66, -6, 81, 92, 14, 13, -2, 72, 7, 60, 15, 9, -66, 55, 16, -37, 50, 1, -31, 8, 17, 84, 6, 55, 64, -45, 4, -2, 14, 59, -68, 27, 93, -3, -12, -71, 45, -6, -36, 92, -26, 44, 44, 30, 45, -48, -62, 63, -1, 92, -30, -91, -44, -73, 6, 28, -75, 67, -6, 34, 33, 56, 44, -70, -18, -68, -96, 76]
        expected_result = 27
        result = solution(arr)
        self.assertEqual(result, expected_result)

    def test_03(self):
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
        expected_result = 0
        result = solution(arr)
        self.assertEqual(result, expected_result)

    def test_04(self):
        arr = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        expected_result = 4950
        result = solution(arr)
        self.assertEqual(result, expected_result)

    def test_05(self):
        arr = [100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100]
        expected_result = 2450
        result = solution(arr)
        self.assertEqual(result, expected_result)

    def test_06(self):
        arr = [4, 8, 10, 6, 8, 6, 10, 6, 10, 6, 4, 10, 10, 6, 4, 6, 6, 4, 6, 6, 6, 10, 8, 4, 10, 4, 10, 2, 2, 2, 6, 4, 6, 4, 6, 10, 8, 8, 4, 10, 10, 4, 10, 10, 8, 8, 2, 8, 6, 8, 10, 8, 2, 10, 2, 6, 10, 10, 8, 10, 4, 8, 2, 10, 2, 6, 6, 2, 6, 4, 6, 6, 8, 4, 10, 2, 4, 4, 2, 8, 8, 4, 6, 10, 2, 2, 6, 10, 10, 8, 6, 8, 2, 6, 4, 2, 10, 2, 10, 4]
        expected_result = 985
        result = solution(arr)
        self.assertEqual(result, expected_result)

    def test_07(self):
        arr = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        expected_result = 2450
        result = solution(arr)
        self.assertEqual(result, expected_result)

    def test_08(self):
        arr = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        expected_result = 1
        result = solution(arr)
        self.assertEqual(result, expected_result)

    def test_09(self):
        arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_result = 4950
        result = solution(arr)
        self.assertEqual(result, expected_result)

    def test_10(self):
        arr = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
        expected_result = 5
        result = solution(arr)
        self.assertEqual(result, expected_result)

    def test_11(self):
        arr = [i for i in range(50)] * 2000  # Creates an array of 100000 elements with 2000 instances of each number from 0 to 49
        expected_result = 2000 * (2000 - 1) // 2 * 50  # Calculate number of pairs
        result = solution(arr)
        self.assertEqual(result, expected_result)
        

if __name__ == "__main__":
    unittest.main()