from matplotlib import pyplot as plt
import numpy as np
from functools import lru_cache


grid_sizes = [4, 8, 16, 32, 64]
lagrange_grid = [[-1 + 2*j/(i) for j in range(i+1)] for i in grid_sizes]
# print(lagrange_grid)

# chebyshev_grid = [[ np.cos( ((2*j+1)*np.pi)/(2*(i+1)) ) for j in range(i+1)] for i in grid_sizes]
# print([f'{x:.3f}' for x in chebyshev_grid[1]])
# print([f'{x:.3f}' for x in chebyshev_grid[2]])

chebyshev_grid= [[ -np.cos( (j*np.pi)/i ) for j in range(i+1)] for i in grid_sizes]
print([f'{x:.3f}' for x in chebyshev_grid[1]])
print([f'{x:.3f}' for x in chebyshev_grid[2]])


def f(x): 
    return 1/(1 + 25*x**2)

def lagrange_basis(n, i, x):
    p = 1
    for j in range(grid_sizes[n]+1):
        if j != i:
            p *= (x - lagrange_grid[n][j])/(lagrange_grid[n][i] - lagrange_grid[n][j])
    return p

def get_lagrange_form(n, x):
    P = 0
    for i in range(grid_sizes[n]+1):
        # ну можно сделать словарик со значениями чтобы не считать лишний раз
        P += f(lagrange_grid[n][i]) * lagrange_basis(n, i, x)
    return P


def get_chebyshev_form(n, x):
    return np.cos(n * np.arccos(x))


@lru_cache(maxsize=None)
def get_Am(n, i, k):
    if k == 0:
        return f(lagrange_grid[n][i])
    else:
        return (get_Am(n, i+1, k-1) - get_Am(n, i, k-1)) / (lagrange_grid[n][i+k] - lagrange_grid[n][i])

def get_coef(nodes):
    f_layer = [f(x) for x in nodes]
    coef = [f_layer[0]]

    for k in range(1, len(nodes)):
        f_layer = [
            (f_layer[i+1] - f_layer[i]) / (nodes[i+k] - nodes[i])
            for i in range(len(f_layer)-1)
        ]
        coef.append(f_layer[0])

    return coef

def get_newton_form(nodes, x):
    m = len(nodes)
    # coef = [get_Am(n, 0, i) for i in range(m)]
    coef = get_coef(nodes)
    S = coef[0]
    p = 1

    for i in range(1, m):
        p *= (x - nodes[i-1])
        S += coef[i] * p
    
    return S



x = np.linspace(-1, 1, 1000)
y_true = f(x)


for i, n in enumerate(grid_sizes):
    # вообще плохо, что я лишний раз высчитываю полином. 
    # y_chebyshev = [get_chebyshev_form(i, t) for t in x]

    # y_lagrange = [get_lagrange_form(i, t) for t in x]
    y_newton = [get_newton_form(chebyshev_grid[i], t) for t in x]

    plt.figure(figsize=(10, 6))

    plt.plot(x, y_true, label='Оригинальная функция', linewidth=2)
    # plt.plot(x, y_lagrange, label='Лагранж')
    plt.plot(x, y_newton, '--', label='Ньютон')
    # plt.plot(x,y_chebyshev,label="Чебышев")
    # plt.ylim(-1.2, 1.2)

    plt.scatter(
        chebyshev_grid[i],
        [get_newton_form(chebyshev_grid[i], t) for t in chebyshev_grid[i]],
        color='black',
        s=20,
        label='точки интерполяции',
        zorder=3
    )
    plt.title(f'Многочлен Чебышева, n={n}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.legend()

    plt.savefig(f'Многочлен Чебышева, n={n}.png', dpi=150)
    plt.close()

# for i, n in enumerate(grid_sizes):
#     y_lagrange = [get_lagrange_form(i, t) for t in x]
#     y_newton = [get_newton_form(i, t) for t in x]
#     # y_chebyshev = [get_chebyshev_form(i, t) for t in x]

#     plt.figure(figsize=(10, 6))

#     plt.plot(x, y_true, label='Оригинальная функция', linewidth=2)
#     plt.plot(x, y_lagrange, label='Лагранж')
#     plt.plot(x, y_newton, '--', label='Ньютон')
#     plt.ylim(-1.2, 1.2)

#     plt.scatter(
#         lagrange_grid[i],
#         [get_lagrange_form(i, t) for t in lagrange_grid[i]],
#         color='black',
#         s=20,
#         label='Interpolation nodes',
#         zorder=3
#     )
#     plt.title(f'Interpolation comparison, n={n}')
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.grid()
#     plt.legend()

#     plt.savefig(f'y_lim(-1.2, 1.2) interpolation_n={n}.png', dpi=150)
#     plt.show()
#     plt.close()
