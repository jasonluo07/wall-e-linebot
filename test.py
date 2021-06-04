import random

letters = [chr(ord('a') + i) for i in range(10)]

for _ in range(10):
    print(letters[random.randrange(10)])
