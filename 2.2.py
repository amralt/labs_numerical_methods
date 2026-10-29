import numpy as np
from matplotlib  import pyplot as plt

eps = np.nextafter(1, 2) - 1


def newton_method(f: callable, iter_f: callable, x):
    count = 0
    table = []
    fx = f(x)
    prev_x = 0
    en = 0
    history_en = []
    history_en2 = []
    prev_en = 0
    while fx >= eps:
        count += 1
        prev_x = x
        x = iter_f(x)
        fx = f(x)
        prev_en=en
        en = abs(0 - x) # x* вроде бы означает корень
        if prev_en != 0:
            history_en.append((count, en/prev_en))
            history_en2.append((count, en/(prev_en**2)))
            print(en/prev_en, en/(prev_en**2))

        table.append((count, x, fx, abs(x - prev_x)))
    return table, history_en, history_en2


def f(x): 
    return pow(x,2) * pow(np.e, x)

def df(x): return -8 * x - np.exp(x)


def iter_formula1(x):
    return (pow(x,2) + x) / (2 + x)

def iter_formula2(x):
    return (pow(x,2)) / (2 + x)


def plot_en(history, label, fname):
    n, r = zip(*history)
    plt.figure(figsize=(6,10))
    plt.plot(n, r, 'o-', label=label)
    plt.title(fname)
    plt.xlabel('n')
    plt.ylabel(label)
    plt.savefig(fname)
    plt.close()
    print("нарисован график", label)


en1, en2 = [], []
nm_1, en1, en2 = newton_method(f, iter_formula1, 1)
print('обычный метод', len(nm_1))
plot_en(en1, 'en/prev_en', 'графики/en prev_en обычный м. Ньютона.svg' )
plot_en(en2, 'en/prev_en', 'графики/en prev_en^2 обычный м. Ньютона.svg' )

# plot_en([(i, nm_1[i][2]) for i in range(len(nm_1))], 'график ошибки |xn+1 − xn| ', 'графики/график ошибки м. Ньютона.svg' )


en1.clear()
en2.clear()
nm_2,en1, en2 = newton_method(f, iter_formula2, 1)
print('модифицированный метод:\nen/prev_en      en/prev_en^2', len(nm_2))
plot_en(en1, 'en/prev_en', 'графики/en prev_en мод. м. Ньютона.svg' )
plot_en(en2, 'en/prev_en', 'графики/en prev_en^2 мод м. Ньютона.svg' )
# en prev_en мод. 
with open('txt/newton_method_1.txt', 'w') as f:
    i = 0
    print(f"n, {' '*10} xn, {' '*10} |f(xn)| {' '*10} |xn+1 − xn| ", file=f)
    for line in nm_1:
        i+=1
        print(i, ":", line, file=f)


with open('txt/newton_method_2.txt', 'w') as f:
    i = 0
    print(f"n, {' '*10} xn, {' '*10} |f(xn)| {' '*10} |xn+1 − xn| ", file=f)
    for line in nm_2:
        i+=1
        print(i, ":", line, file=f)

# print(nm_1)
# print(nm_2)

