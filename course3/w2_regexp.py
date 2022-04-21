import re


def _findall(regexp):
    text = """
    a=1
    a=+1
    a=-1
    a=b
    a=b+100
    a=b-100
    
    b+=10
    b+=+10
    b+=-10
    b+=b
    b+=b+100
    b+=b-100
    
    c-=101
    c-=+101
    c-=-101
    c-=b
    c-=b+101
    c-=b-101
    """

    return re.findall(regexp, text)


def calculate(data, findall):
    arifmeticRegexp = re.compile(r"""
    ([abc])
    ([\+\-]?)
    =
    ([abc]?)
    ([\+\-]?(?:\d+)?)
    """, re.VERBOSE)
    matches = findall(
        arifmeticRegexp)  # Если придумать хорошую регулярку, будет просто
    # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
    for v1, s, v2, n in matches:
        # Если бы могло быть только =, вообще одной строкой все считалось бы, вот так:
        right = data.get(v2, 0) + int(n or 0)
        if s == "":
            data[v1] = right
        else:
            if s == '+':
                data[v1] += right
            elif s == '-':
                data[v1] -= right

    return data


if __name__ == "__main__":
    result = calculate({'a': 1, 'b': 2, 'c': 3}, _findall)
    correct = {"a": -98, "b": 196, "c": -686}
    if result == correct:
        print("Correct")
    else:
        print("Incorrect: %s != %s" % (result, correct))
