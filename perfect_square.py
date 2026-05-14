def solution(arr):
    
    results = []
    for i in arr:
        closest = closest_perfect_square(i)
        results.append(calc_factors(closest))
        
        print(calc_factors(closest))
        
    return results

    
def calc_factors(n):
    if n <= 1:
        return n
    
    total_factors = 1
    d = 2
    
    while d * d <= n:
        if n % d == 0:
            expoentes = 0
            while n % d == 0:
                expoentes += 1
                n //= d
                
            total_factors *= (expoentes + 1)
        
        d += 1
        
    if n > 1:
        total_factors *= 2
        
    return total_factors
        
    
def closest_perfect_square(n):
    real_sqrt = n ** (.5)
    
    low = int(real_sqrt)
    high = low + 1
    
    low_square = low ** 2
    high_square = high ** 2
    
    if abs(low_square - n) <= abs(high_square - n):
        return low_square
    
    return high_square


solution([10000])