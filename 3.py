import numpy as np
import matplotlib.pyplot as plt
N = 50
tau=1
r=1


L=0.5

matr_t = []

def criteria(temps_1, temps_2):
    mx = 0
    for i in range(len(temps_1)):
        mx = max(mx, abs(temps_1[i]-temps_2[i]))
    return mx/tau < 1e-5


def solve_system(a, b, c ,d):
    n = len(d)
    x = [0]*n
    p = [0]*n
    q = [0]*n

    p[0], q[0] = c / b, d[0]/b
    
    for i in range(1, n-1):
        betta = b - a*p[i-1]
        p[i] = c/betta
        q[i] = (d[i] - a*q[i-1])/(betta)  

    betta = b - a*p[n-2]
    q[n-1] = (d[n-1] - a*q[n-2])/(betta)  

    # обратный ход
    x[-1] = q[-1]
    for i in range(len(x)-2,-1,-1): 
        x[i] = q[i] - p[i]*x[i+1]

    return x

# print(solve_system(-1, 3, -1, [2, 1, 2]))

def get_start_temp(N:int):
    h = 0.01
    temp = [0]*N
    for i in range(N):
        x = i*h
        temp[i] = 20+80*(np.cos(0.5*np.pi*x/L)**2)
    return temp


count_t = 0
temps = get_start_temp(N+1)
temps[0] = 100
temps[-1] = 20
# print(next_temps)
all_history = []

while True:
    count_t += 1

    d = temps[1:-1].copy()
    d[0] += temps[0]
    d[-1] += temps[-1]

    next_temps = temps.copy()
    next_temps[1:-1] = solve_system(-1, 3, -1, d)
    
    
    if criteria(temps, next_temps):
        break
    all_history.append(temps)
    temps = next_temps



print(next_temps)
print("количество временных промежутков ", count_t)


# 1 график
plt.figure(figsize=(10, 5))
history=[]
for i in [0, count_t//10, count_t//4, count_t//2, count_t-2]:
    history.append((i, all_history[i]))

x = np.linspace(0, L, N + 1)
    
for step, temp_profile in history:
    t_current = step * tau
    plt.plot(x, temp_profile, label=f"t = {t_current:.2f} с (шаг {step})", linewidth=2)

plt.title("Пространственные сечения T(x, t)")
plt.xlabel("x ")
plt.ylabel("Температура °C")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("1.Пространственные сечения.svg")
plt.close()


# 2 график
temp1 = []
temp2 = []
temp3 = []
indices_x = [int(N//4), int(N//2), int(3*N//4)]

for i in range(count_t-1):
    temp1.append(all_history[i][indices_x[0]])
    temp2.append(all_history[i][indices_x[1]])
    temp3.append(all_history[i][indices_x[2]])
times = [i for i in range(count_t-1)]

plt.figure(figsize=(10, 5))
plt.plot(times, temp1, label=f"x = L/4 = {L/4:.3f} м", linewidth=2)
plt.plot(times, temp2, label=f"x = L/2 = {L/2:.3f} м", linewidth=2)
plt.plot(times, temp3, label=f"x = 3L/4 = {3*L/4:.3f} м", linewidth=2)

# plt.figure(figsize=(10, 5))
plt.title("Временные сечения.")
plt.xlabel("x ")
plt.ylabel("время t, с")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("2. Временные сечения.svg")
plt.close()


def plot_heatmap(full_history, N, L, count_t, tau):
    plt.figure(figsize=(10, 6))
    
    x = [i * L / N for i in range(N + 1)]
    times = [i * tau for i in range(count_t-1)]
    
    c = plt.pcolormesh(x, times, full_history, cmap='cividis', shading='nearest')
    
    plt.colorbar(c, label="Температура, °C")
    plt.title(f"Карта температуры в плоскости (x, t) размер сетки: {N}")
    plt.xlabel("Координата x, м")
    plt.ylabel("Время t, с")
    plt.tight_layout()
    plt.savefig(f'3. Карта температуры N={N}.png')
    plt.close()


def print_table(full_history, indices_x, L, count_t, tau):    
    n = len(full_history)
    t_star = (count_t - 1) * tau
    t_targets = [0, 0.25 * t_star, 0.5 * t_star, t_star]
    
    print(f"\nТаблица значений (t_* = {t_star:.2f} с)")
    print("-" * 65)
    print(f"{'t, с':<10} | {'T(L/4)':<12} | {'T(L/2)':<12} | {'T(3L/4)':<12}") # как в 2 пункте
    print("-" * 65)
    
    for t in t_targets:
        idx = int(round(t / tau))
        # Ограничиваем индекс реальным размером истории
        if idx >= n:
            idx = n - 1
            
        val_1 = full_history[idx][indices_x[0]]
        val_2 = full_history[idx][indices_x[1]]
        val_3 = full_history[idx][indices_x[2]]
        
        # Выводим фактическое время, соответствующее этому слою (idx * tau)
        print(f"{idx * tau:<10.2f} | {val_1:<12.2f} | {val_2:<12.2f} | {val_3:<12.2f}")

plot_heatmap(all_history, N, L, count_t, tau)
print_table(all_history, indices_x, L, count_t, tau)