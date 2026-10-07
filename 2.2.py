import numpy as np

eps = np.nextafter(1, 2) - 1


def newton_method(f: callable, iter_f: callable, x):
    count = 0
    table = []
    fx = f(x)
    prev_x = 0
    en = 0
    prev_en = 0
    while fx >= eps:
        count += 1
        prev_x = x
        x = iter_f(x)
        fx = f(x)
        prev_en=en
        en = abs(0 - x) # x* вроде бы означает корень
        if prev_en != 0:
            print(en/prev_en, en/(prev_en**2))

        table.append((count, x, fx, abs(x - prev_x)))
    return table


def f(x): 
    return pow(x,2) * pow(np.e, x)

def df(x): return -8 * x - np.exp(x)


def iter_formula1(x):
    return (pow(x,2) + x) / (2 + x)

def iter_formula2(x):
    return (pow(x,2)) / (2 + x)

nm_1 = newton_method(f, iter_formula1, 1)
print('обычный метод', len(nm_1))
nm_2 = newton_method(f, iter_formula2, 1)
print('модифицированный метод:\nen/prev_en      en/prev_en^2', len(nm_2))


with open('newton_method_1.txt', 'w') as f:
    for line in nm_1:
        print(line, file=f)


with open('newton_method_2.txt', 'w') as f:
    for line in nm_2:
        print(line, file=f)

# print(nm_1)
# print(nm_2)

