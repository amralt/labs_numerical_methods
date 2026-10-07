import numpy as np

eps = np.nextafter(1, np.float32(2)) - 1
eps *= 100
MAX_ITER = 10000   
x_ref = 0.7034395711636399 # тут до 2^(-50)

def f(x):
    return 4*(1-x**2)- np.exp(x)

def df(x): return -8 * x - np.exp(x)


def check_stop(crit, eps, fx, x, x_prev, a, b):
    if crit == 'K1': return abs(fx) <= eps
    if crit == 'K2': return abs(x - x_prev) <= eps
    if crit == 'K3': return abs(x - x_prev) <= eps * (1 + abs(x))
    if crit == 'K4': return (b - a) / 2 <= eps
    return False


def bisection(f: callable, a: float, b: float, crit: str, e=eps) -> tuple:
    if f(a) * f(b) > 0:
        return None
    count = 0
    fa = f(a); fb=f(b)
    x_prev = a
    while count < MAX_ITER:
        c = (a+b)/2
        fc = f(c)
        count += 1
        if check_stop(crit, eps, fc, c, x_prev, a, b):
            return (count, c, fc, abs(c - x_ref))
        # table.append((count, c, fc, abs(c - x_ref) ))
        if fc*fa < 0:
            b = c; fb=fc
        else:
            a = c; fa=fc
        x_prev=c
            
    return (count, c, fc, abs(c - x_ref))
    
    
def regula_falsi(f: callable, a: float, b: float, crit):
    counter = 0
    fa = f(a); fb=f(b)
    x_prev = a

    while counter < MAX_ITER:
        c = a - fa*  (b-a)/(fb-fa) 
        fc = f(c)
        counter+=1
        if check_stop(crit, eps, fc, c, x_prev, a, b):
            return (counter, c, fc, abs(c - x_ref))
        
        if fc*fa < 0:
            b = c; fb = fc
        else:
            a = c; fa = fc 
        x_prev = c

    return (counter, c, fc, abs(c - x_ref))



def illinois_method(f: callable, a: float, b: float, crit: str):
    counter = 0
    ka, kb = 0, 0
    fa = f(a); fb=f(b)
    x_prev = a
    while counter < MAX_ITER:
        c = a - fa*  (b-a)/(fb-fa) 
        fc = f(c)
        counter += 1
        if check_stop(crit, eps, fc, c, x_prev, a, b):
            return (counter, c, fc, abs(c - x_ref))

        if fc*fa < 0:
            b = c
            fb = fc
            ka = ka + 1
            kb = 0
            if ka >= 2:
                fa = fa/2

        else:
            a = c
            fa = fc
            ka = 0
            kb = kb + 1
            if kb >= 2:
                fb = fb/2
        x_prev=c

    return (counter, c, fc, abs(c - x_ref))

def newton_method(f: callable, iter_f: callable, x, crit: str):
    count = 0
    table = []
    fx = f(x)
    x_prev = 0
    while count < MAX_ITER:
        count += 1
        x_prev = x
        x = iter_f(x)
        fx = f(x)
        if check_stop(crit, eps, fx, x, x_prev, 0, 0):
            return (count, x, fx, abs(x - x_ref))

    return (count, x, fx, abs(x - x_ref))

def iterate(x):
    return x- (4-4*x*x - pow(np.e, x))/(-8*x-pow(np.e, x))


def secant_method(f: callable, x0, x1, crit):
    f0 = f(x0); f1 = f(x1)
    count = 0
    while count < MAX_ITER:
        count += 1
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        f2 = f(x2)
        if check_stop(crit, eps, f2, x2, x1, 0, 0):
            return (count,x2,f2 ,abs(x2-x_ref), )

        x0, f0 = x1, f1
        x1, f1 = x2, f2

    return (count,x2,f2 ,abs(x2-x_ref), )


def stefan_method(f: callable, x, crit):
    count = 0
    table = []
    fx = f(x)
    x_prev = 0
    while count < MAX_ITER:
        count += 1
        x_prev = x
        fx = f(x)
        x = x - (fx**2)/(f(x+fx) - fx)
        if check_stop(crit, eps, fx, x, x_prev, 0, 0):
            return (count, x, fx, abs(x - x_ref))

    return (count, x, fx, abs(x - x_ref))


a0, b0 = 0, 1
x0 = 0.5


# x_ref = bisection(f, a0, b0, pow(2, -60))
# print(x_ref)

criteria_loc=['K1', 'K2', 'K3', 'K4']
criteria=['K1', 'K2', 'K3']



results={
    'Бисекция': [],
    'Ложное положение': [],
    'Иллинойс': [], 
    'Ньютон': [],
    'Стэфан': [], 
    'Секущих': []
}

for i in criteria_loc:
    results['Бисекция'].append(bisection(f, a0, b0, i))
    results['Ложное положение'].append(regula_falsi(f, a0, b0, i))
    results['Иллинойс'].append(illinois_method(f, a0, b0, i))

for i in criteria:
    results['Ньютон'].append(newton_method(f, iterate, x0, i))
    results['Стэфан'].append(stefan_method(f, x0, i))
    results['Секущих'].append(secant_method(f, a0, b0, i))



methods_order = ['Бисекция', 'Ложное положение', 'Иллинойс', 'Ньютон', 'Стэфан', 'Секущих']
crits_order = [criteria_loc, criteria_loc, criteria_loc, criteria, criteria, criteria]

with open('2.3_results_eps*100.txt', 'w', encoding='utf-8') as file:
    header = f"{'Метод':<18} | {'Крит':<4} | {'n':<5} | {'x':<12} | {'|f(x)|':<12} | {'|x - x_ref|':<14}"
    file.write(header + "\n")
    file.write("-" * len(header) + "\n")
    
    for name, crits in zip(methods_order, crits_order):
        for idx, lines in enumerate(results[name]):
            crit = crits[idx]
            n, x_hat, fx, err = lines
            row = f"{name:<18} | {crit:<4} | {n:<5} | {x_hat:<12.8f} | {abs(fx):<12.2e} | {err:<14.2e}"
            file.write(row + "\n")