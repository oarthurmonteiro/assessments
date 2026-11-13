import os

#
# Complete the 'isBalanced' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def isBalanced(s):
    # Write your code here
    # string_size = len(s)
    # if string_size % 2 != 0:
    #     return "NO"

    brackets = {
        "{": "}",
        "[": "]",
        "(": ")",
    }

    # ((()))
    stack = []
    for char in s:
        if char in brackets:
            stack.append(char)
            continue

        if len(stack) <= 0:
            return "NO"

        b = stack.pop()
        if brackets[b] != char:
            return "NO"

    return "YES"



if __name__ == '__main__':
    fptr = open("result.txt", 'w')

    t = int(input().strip())

    for t_itr in range(t):
        s = input()

        result = isBalanced(s)

        fptr.write(result + '\n')

    fptr.close()
