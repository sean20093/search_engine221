import math

DCG_divider = [1.0, 1.0, 1.59, 2.0, 2.32]
sequence = [5, 4, 3, 2, 1]


def DCG_calculate(sequence, DCG_divider):
    i = -1
    result = 0
    for score in sequence:
        i += 1
        if score is 0:
            continue
        result += score/DCG_divider[i]
    return result


result = DCG_calculate(sequence, DCG_divider)
print result

