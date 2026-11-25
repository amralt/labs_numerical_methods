from matplotlib import pyplot as plt
import numpy as np

grid_sizes = [4, 8, 16, 32, 64]
lagrange_grid = [[-1 + 2*j/(i) for j in range(i+1)] for i in grid_sizes]
chebyshev_grid= [[ -np.cos( (j*np.pi)/i ) for j in range(i+1)] for i in grid_sizes]

def f(x): 
    return 1/(1 + pow(25*x, 2))


def solve_system(a, b, c ,d):
    n = len(d)
    x = [0]*n
    p = [0]*n
    q = [0]*n

    p[0], q[0] = c[0] / b[0], d[0]/b[0]
    
    for i in range(1, n-1):
        betta = b[i] - a[i]*p[i-1]
        p[i] = c[i]/betta
        q[i] = (d[i] - a[i]*q[i-1])/(betta)  

    betta = b[n-1] - a[n-1]*p[n-2]
    q[n-1] = (d[n-1] - a[n-1]*q[n-2])/(betta)  

    # обратный ход
    x[-1] = q[-1]
    for i in range(len(x)-2,-1,-1): 
        x[i] = q[i] - p[i]*x[i+1]

    return x


x = np.linspace(-1, 1, 1000)
y_true = f(x)

def draw_spline(n, nodes, coefficients, points, name):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y_true, label='Оригинальная функция', linewidth=2)
    plt.plot(x, points, '--', label='Сплайн')
    plt.scatter(
        nodes[grid_sizes.index(n)],
        [S_i(t, get_index_by_t(t, nodes[grid_sizes.index(n)]), nodes[grid_sizes.index(n)], h, coefficients) for t in nodes[grid_sizes.index(n)]],
        color='black',
        s=20,
        label='точки интерполяции',
        zorder=3
    )
    plt.title(f'Сплайн с сеткой {name}, n={n}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.legend()

    plt.savefig(f'сплайны/Сплайн с сеткой {name}, n={n}.png', dpi=150)
    plt.close()



def S_i(x, i, nodes, h, coef):
    return ( coef[i-1]/(6*h[i-1]) ) * (nodes[i] - x)**3 \
            + ( coef[i]/(6*h[i-1]) ) * (x - nodes[i-1])**3 \
            + ( f(nodes[i-1]) - (coef[i-1]*h[i-1]**2)/6 ) * (nodes[i] - x)/h[i-1] \
            + ( f(nodes[i]) - (coef[i]*h[i-1]**2)/6 ) * (x - nodes[i-1])/h[i-1]

def get_index_by_t(t, nodes):
    for i in range(len(nodes)-1):
        if nodes[i] <= t <= nodes[i+1]:
            return i+1
    return -1

for k, n in enumerate(grid_sizes):
    nodes = lagrange_grid[k]
    h = np.diff(nodes)
    values = [f(t) for t in nodes]

    a_list = [0.0] * (n - 1)
    b_list = [0.0] * (n - 1)
    c_list = [0.0] * (n - 1)
    d_list = [0.0] * (n - 1)

    for r in range(n - 1):
        i = r + 1
        b_list[r] = (h[i - 1] + h[i]) / 3

        if r > 0:
            a_list[r] = h[i - 1] / 6
        if r < n - 2:
            c_list[r] = h[i] / 6
        d_list[r] = (
            (values[i + 1] - values[i]) / h[i]
            - (values[i] - values[i - 1]) / h[i - 1]
        )

    coefficients = solve_system(
        a_list, b_list, c_list, d_list
    )
    M = [0.0] + coefficients + [0.0]

    points = [S_i(t, get_index_by_t(t, lagrange_grid[k]), lagrange_grid[k], h, M) for t in x]
    points_Ch = [S_i(t, get_index_by_t(t, chebyshev_grid[k]), chebyshev_grid[k], h, M) for t in x]
    draw_spline(n, lagrange_grid, M, points, "Лагранжа")
    draw_spline(n, chebyshev_grid, M, points_Ch, "Чебышева")

