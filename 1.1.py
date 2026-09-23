from numpy import float32, float64, nextafter, inf, log2, errstate


def find_E_min(num, eps):
    e_min = 0
    while num * (1 + eps) != num:
        num /= 2
        e_min -= 1
    return e_min

def find_E_max(n: float32 | float64):
    e_max = 0
    with errstate(over='ignore'):
        while n*2 > n:  
            n *= 2
            e_max += 1
    return e_max


def find_eps(num, eps):
    while num + eps/2 != num:
        eps = eps/2
    return eps

num32 = float32(1.0)
eps32 = float32(1.0)

eps32 = find_eps(num32, eps32)
e32 = nextafter(1, float32(2)) -1
print('nextafter eps: ', e32)
print('eps: ', eps32)
print('nextafet eps==eps? ', e32==eps32)
print('1 + eps/2:', 1 + eps32/2, '\n1+ eps: ' , f'{1 + eps32:.20}', '\neps/2:', eps32/2)

num64 = float64(1.0)
eps64 = float64(1.0)
eps64 = find_eps(num64, eps64)
print('\n\nпроверка для 64 битных чисел: ')
print('1 + eps/2:', 1 + eps64/2, '\n1+ eps: ' , f'{1 + eps64:.20}', '\neps/2:', eps64/2)
print('\n')


small_num = float64(1e-16)
print(small_num)
print('(1 + 10^16) + 10^16: ', (1+small_num)+small_num)
print('1 + (10^16 + 10^16): ', 1+ (small_num + small_num))
print('1e-16 < eps/2: ', small_num < eps64/2)
print('1e-16 + 1e-16 < eps/2: ',small_num + small_num < eps64/2)
#p = print(len('5.960464477539063'))

print(f'формат{' '*6}p{' '*3}Emin{' '*3}Emax{' '*5}ϵ{' '*23}u')
p32 = 1-log2(eps32)

print(f'binary32: {p32} | {find_E_min(float32(1.0), eps32)} | {find_E_max(float32(1.0))} | {eps32} | {eps32/2}' )
print(f'binary64: {1-log2(eps64)} | {find_E_min(float64(1.0), eps64)} | {find_E_max(float64(1.0))} | {eps64} | {eps64/2}')