from pathlib import Path
with Path(Path(__file__).parent, "data").open() as f:
    RAW = f.read().strip().split('\n')

BRACKETS = {'{': '}', '(': ')', '[': ']', '<': '>'}
REV = {val: key for key, val in BRACKETS.items()}
SCORE = {'(': 3, '[': 57, '{': 1197, '<': 25137}
SCORE2 = {'(': 1, '[': 2, '{': 3, '<': 4}
total = 0
scores = []
for line in RAW:
    stack = []
    legal = True
    for ch in line:
        if ch in BRACKETS:
            stack.append(ch)
        elif REV[ch] == stack[-1]:
            stack.pop()
        else:
            open = REV[ch]
            total += SCORE[open]
            legal = False
            break

    if legal:
        score = 0
        for ch in reversed(stack):
            score *= 5
            score += SCORE2[ch]
        scores.append(score)

scores.sort()
print(total)
print(scores[len(scores)//2])
