from numpy import float32, float64, log
import matplotlib.pyplot as plt

ln2=log(2)
N = 8


def find_sum(n, order=0, num_type=float32):
    s = num_type(0.0)
    l = range(1, n)
    if(order == -1):
        l=reversed(l)
    
    for k in l:
        s += num_type(pow(-1, k+1)/k)
    return s


def find_sep_sum(n, num_type=float32):
    possitive = 0
    negative = 0
    for k in range(1,n+1, 2):
        possitive += num_type(1/k)
    for k in range(2, n+1, 2):
        negative+=num_type(1/(k))
    return num_type(possitive - negative)


def find_error(n):
    return abs(find_sum(n) - float32(ln2))

n100 = 100
n10k = 10_000

S10k = find_sum(n10k)
error_S10k = find_error(n10k)

print("error n=10k:", error_S10k)
print("оценка усечения: ", error_S10k<= float32(1/(n10k+1)))
print("ошибка усечения: ", error_S10k - 1/(n10k+1))


err_usech_fwd, err_usech_bwd, err_usech_sep = [], [], []
err_comp_fwd, err_comp_bwd, err_comp_sep = [], [], []

for i in range(1, N):
    n = pow(10, i)

    s64 = find_sum(n, 0, float64)

    s32_fwd = find_sum(n, 0, float32)
    s32_bwd = find_sum(n, -1, float32)
    s32_sep = find_sep_sum(n, float32)

    # ошибка усечения
    err_usech_fwd.append(abs(s32_fwd - ln2))
    err_usech_bwd.append(abs(s32_bwd - ln2))
    err_usech_sep.append(abs(s32_sep - ln2))

    # ошибка вычислений
    err_comp_fwd.append(abs(s32_fwd - s64))
    err_comp_bwd.append(abs(s32_bwd - s64))
    err_comp_sep.append(abs(s32_sep - s64))

    print(f"слева направо n={n}: ", s32_fwd)
    print(f"справа налево n={n}: ", s32_bwd)
    print(f"раздельно n={n}: ", s32_sep)
    print()


# я не понял что значит повышенная точность, буду использовать float64
s = 0
for k in range(1, n10k):
    s += float64(pow(-1, k+1)/k)
print("повышщенная точность : ",s)

print("\n|̂ Sn − ln 2| и |̂ Sn − Sn|.")

print("прямая: ", abs(find_sum(n10k, 0)-log(2)), " ", abs(find_sum(n10k, 0) - find_sum(n10k, 0, float64)))
print("обратно: ", abs(find_sum(n10k, -1)-log(2)), " ", abs(find_sum(n10k, -1) - find_sum(n10k, -1, float64)))
print("раздельно: ", abs(find_sep_sum(n10k)-log(2)), " ", abs(find_sep_sum(n10k) - find_sep_sum(n10k, float64)))


# пусть по y - ошибка по x - n

n_values=[pow(10,i) for i in range(1,N)]
plt.figure(figsize=(10, 5))
plt.loglog(n_values, err_usech_fwd, 'o-', label='усечения (вперед)')
plt.loglog(n_values, err_usech_bwd, 's-', label='усечения (назад)')
plt.loglog(n_values, err_usech_sep, '^-', label='усечения (раздельно)')

plt.loglog(n_values, err_comp_fwd, 'o--', label='Вычислительная (вперед)')
plt.loglog(n_values, err_comp_bwd, 's--', label='Вычислительная (назад)')
plt.loglog(n_values, err_comp_sep, '^--', label='Вычислительная (раздельно)')

plt.yscale("log") 
plt.xlabel("n")
plt.ylabel("ошибка")
plt.legend()
plt.show()
plt.savefig('график ошибок.png')