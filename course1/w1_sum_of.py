"""
Начало.
"""


if __name__ == '__main__':
    import sys
    digit_string = sys.argv[1]
    sum = 0
    for it in digit_string:
        sum += int(it)
    print(sum)

"""
for i,c in enumerate('bob'):
    print('{}: {}'.format(c,i))

b: 0
o: 1
b: 2
"""