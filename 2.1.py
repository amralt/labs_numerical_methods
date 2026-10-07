import numpy as np

eps = np.nextafter(1, 2) - 1
g = 9.8
t = 10
m=68.1
gm = g*m

def Bolc_Coshi(f: callable, *args, **kwargs):
    ...

def bisection(f: callable, a: float, b: float) -> tuple:
    if f(a) * f(b) > 0:
        return None
    counter = 0
    fa = f(a); fb=f(b)
    while b-a >= eps:
        c = (a+b)/2
        fc = f(c)
        counter += 1
        if fc == 0:
            return c, counter

        if fc*fa < 0:
            b = c
            fb=fc
        else:
            a = c
            fa=fc
    return c, counter
    
    
def regula_falsi(f: callable, a: float, b: float):
    if f(a) * f(b) > 0:
            return None
    counter = 0
    fa = f(a); fb=f(b)
    stable_a,stable_b = 0,0
    max_stable = 0
    side = ''
    while b-a >= eps:
        c = a - fa*  (b-a)/(fb-fa) 
        fc = f(c)
        counter+=1
        if fc == 0:
            return c, counter, side, max_stable

        if fc*fa < 0:
            # свдинули правую сторону.
            b = c
            fb = fc
            if stable_b > 0: # меняем сторону
                if max_stable < stable_b:
                    side='right'
                max_stable = max(stable_b, max_stable) 

            stable_a += 1
            stable_b = 0 
        else:
            a = c
            fa = fc 
            if stable_a > 0: 
                if max_stable < stable_a:
                    side='left'
                max_stable = max(stable_a, max_stable); 
            
            stable_b += 1
            stable_a = 0

    if stable_a > stable_b:
        side = 'left'
    else:
        side = 'right'
    
    return c, counter, side, max_stable
    

def illinois_method(f: callable, a: float, b: float):
    if f(a) * f(b) > 0:
        return None
    counter = 0
    ka, kb = 0, 0
    fa = f(a); fb=f(b)
    while b-a >= eps:
        c = a - fa*  (b-a)/(fb-fa) 
        fc = f(c)
        counter += 1
        if fc == 0:
            return c, counter

        if f(c)*f(a) < 0:
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

    return (c, counter)

def v(c :float):
    if c == 0:
        return -1
    return (1-pow(np.e, -(c/m)*t ))*gm/c - 40

# 1. надо найти локализацию
print(v(1), v(10))
print(v(10), v(100)) 

a, b = 10, 100

bs, bs_count = bisection(v,a,b)
rgl_fls, rgl_fls_count, stabled_side, mxstable = regula_falsi(v, a, b)
illinois, illinois_count = illinois_method(v ,a, b)


print(f"Бисекция:     {bs:.10f}, Итераций = {bs_count}")
print(f"Регула Фалси: {rgl_fls:.10f}, Итераций = {rgl_fls_count},  \n  неподвижный конец: {stabled_side}, сколько раз остановился на этой стороне: {mxstable}")
print(f"Иллинойс:     {illinois:.10f}, Итераций = {illinois_count}")


# TODO: надо езе и кол-во итераций в методах считать.. и график выводить