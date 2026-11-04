from collections import defaultdict, deque
from string import ascii_lowercase


def solution(beginWord: str, endWord: str, wordList: list[str]) -> int:
    queue = deque([(1, beginWord)])
    visited = set()
    word_list_patterns = generate_pattern_map(wordList)

    while len(queue) > 0:
        level, word = queue.popleft()
        if word == endWord:
            return level

        if word in visited:
            continue

        for idx in range(len(word)):
            pattern = word[:idx] + "*" + word[idx+1:]
            for candidate_word in word_list_patterns[pattern]:
                queue.append((level + 1, candidate_word))

        visited.add(word)

    return 0

def generate_pattern_map(word_list: list[str]) -> defaultdict[str, set[str]]:
    size = len(word_list[0])
    word_patterns: dict[str, set[str]] = defaultdict(set)
    for word in word_list:
        for idx in range(size):
            pattern = word[:idx] + "*" + word[idx+1:]
            word_patterns[pattern].add(word)

    return word_patterns


# Some dude is other world
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        n = len(beginWord)
        m = len(wordList)

        wl = set(wordList)
        if endWord not in wl:
            return 0

        vp = set()
        c = 1
        fq, bq = deque([beginWord]), deque([endWord])
        fv, bv = {beginWord}, {endWord}
        while fq or bq:
            if (fq and bq and len(fq) > len(bq)) or not fq:
                fq, bq = bq, fq
                fv, bv = bv, fv

            for _ in range(len(fq)):
                w = fq.popleft()
                for t in range(n):
                    pre, suf = w[:t], w[t + 1 :]

                    p = pre + "*" + suf
                    if p in vp:
                        continue
                    vp.add(p)

                    for ch in ascii_lowercase:
                        if ch == w[t]:
                            continue
                        aw = pre + ch + suf
                        if aw not in wl:
                            continue
                        if aw in bv:
                            return c + 1
                        if aw not in fv:
                            fv.add(aw)
                            fq.append(aw)

            c += 1

        return 0

beginWord = "hit"
endWord = "cog"
wordList = ["hot","dot","dog","lot","log","cog"]
# print(generate_pattern_map(wordList))
# exit(1)

print(solution(beginWord, endWord, wordList))
{
    '*it': [],
    'h*t': ['hot'],
    'hi*': [],
    '*ot': ['hot', 'dot', 'lot'],
    'ho*': ['hot'],
    'd*t': ['dot'],
    'do*': ['dot', 'dog'],
    'l*t': ['lot'],
    'lo*': ['lot', 'log'],
    '*og': ['dog', 'log', 'cog'],
    'd*g': ['dog'],
    'l*g': ['log'],
    'c*g': ['cog'],
    'co*': ['cog']
}
