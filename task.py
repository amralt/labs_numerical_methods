

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

n= 3
a = [1 for _ in range(n)]
q = [1 for _ in range(n)]
y = 2/3
k = 1
s = 3-1
#T = []

coef_b = [a[i] + 2 for i in range(n)]
coef_a = [-1]*n
coef_c = [-1]*n

e_k = [0]*n
e_k[k] = 1

T_0 = solve_system(coef_a, coef_b, coef_c, q)
T_1 = solve_system(coef_a, coef_b, coef_c, e_k)
print(T_0, T_1)
p = (y - T_0[s]) / T_1[s]
print(p)