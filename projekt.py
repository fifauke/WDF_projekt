import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as ani

# Cases
# 1: v_f = v_gr
# 2: v_f < v_gr
# 3: v_f < 0 v_gr > 0
# 4: v_f > 0 v_gr < 0
# 5: v_f > v_gr
case = 1

k1 = 2 * np.pi / 0.55  # liczba falowa dla pierwszej fali
k2 = 2 * np.pi / 0.49 # liczba falowa dla drugiej fali


# wyliczanie funkcji
if case == 1:
    plot_title = r'$v_\mathrm{grupowa} = v_\mathrm{fazowa}$'
    dt_plot = np.pi / 200   # krok czasowy
    n_points = 100 * 4 * 2   # liczba punktów
    f1 = lambda x: np.sin(k1 * x) # elastyczna funkcja
    f2 = lambda x: np.sin(k2 * x)
    f = lambda x: f1(x) + f2(x) # superpozycja fal
elif case == 2:
    plot_title = r'$v_\mathrm{fazowa} <  v_\mathrm{grupowa}$'
    dt_plot = np.pi / 400
    n_points = 100 * 4 * 2
    f1 = lambda x: np.sin(k1 * x)
    f2 = lambda x: np.sin(k2 * x)
    f = lambda x: f1(x) + f2(x)
elif case == 3:
    plot_title = r'$v_\mathrm{fazowa} < 0 v_\mathrm{grupowa} > 0$'
    dt_plot = np.pi / 400
    n_points = 100 * 4 * 2
    f1 = lambda x: np.sin(k2 * x)
    f2 = lambda x: np.sin(k1 * x)
    f = lambda x: f1(x) + f2(x)
elif case == 4:
    plot_title = r'$v_\mathrm{fazowa} > 0 v_\mathrm{grupowa} < 0$'
    dt_plot = np.pi / 400
    n_points = 100 * 4 * 2
    f1 = lambda x: np.sin(k2 * x)
    f2 = lambda x: np.sin(k1 * x)
    f = lambda x: f1(x) + f2(x)
elif case == 5:
    k3 = 2 * np.pi / 2
    k4 = 2 * np.pi / 0.2
    plot_title = r'$v_\mathrm{fazowa} > v_\mathrm{grupowa}$'
    dt_plot = np.pi / 400
    n_points = 100 * 4 * 2
    f1 = lambda x: np.sin(k3 * x)
    f2 = lambda x: np.sin(k4* x)
    f = lambda x: f1(x) * f2(x)

n_frames = round(2 * np.pi / dt_plot * 4)

# wartość x i y
x = np.linspace(0, 2*np.pi, n_points)
y = f(x)

# inicjalizacja wykresów
fig, (ax_f1, ax_f2, ax_wave) = plt.subplots(nrows=3, figsize=(15, 8), sharex=True)

# wykres superpozycji
wave, = ax_wave.plot(x, y, "-", color='xkcd:blue', linewidth=2)
ax_wave.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax_wave.set_xticklabels((r'0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'))
ax_wave.set_yticks((-1, 0, 1))
ax_wave.set_xlim(np.amin(x), np.amax(x))
ax_wave.grid(True)
ax_wave.tick_params(axis='both', which='both', direction='in', top=True, right=True)
ax_wave.tick_params(axis='both', labelsize=18)
ax_wave.set_title(plot_title, fontsize=20)

# wykres f1
f1_line, = ax_f1.plot(x, f1(x), "-", color='xkcd:red', linewidth=2)
ax_f1.set_yticks((-1, 0, 1))
ax_f1.grid(True)
ax_f1.tick_params(axis='both', which='both', direction='in', top=True, right=True)
ax_f1.set_title('Funkcja f1', fontsize=16)

# wykres f2
f2_line, = ax_f2.plot(x, f2(x), "-", color='xkcd:green', linewidth=2)
ax_f2.set_yticks((-1, 0, 1))
ax_f2.grid(True)
ax_f2.tick_params(axis='both', which='both', direction='in', top=True, right=True)
ax_f2.set_title('Funkcja f2', fontsize=16)

# zmiana fali i funkcji w czasie: f(x) -> f(x - omega*t)
def shift(t, omega1=1):
    if case == 1:
        new_f1 = f1(x - omega1 * t)
        new_f2 = f2(x - omega1 * t)
        new_y = f1(x - omega1 * t) + f2(x - omega1 * t)
    elif case == 2:
        new_f1 = f1(x - omega1 * t)
        new_f2 = f2(x - 2 * omega1 * t)
        new_y = f1(x - omega1 * t) + f2(x - 2 * omega1 * t)
    elif case == 3:
        new_f1 = f1(x - omega1 * t)
        new_f2 = f2(x + 2 * omega1 * t)
        new_y = f1(x - omega1 * t) + f2(x + 2 * omega1 * t)
    elif case == 4:
        new_f1 = f1(x - omega1 * t)
        new_f2 = f2(x - 2 * omega1 * t)
        new_y = f1(x - omega1 * t) + f2(x - 2 * omega1 * t)
    elif case == 5:
        new_f1 = f1(x - omega1 * t)
        new_f2 = f2(x - 2 * omega1 * t)
        new_y = f1(x - omega1 * t) * f2(x - 2 * omega1 * t)

    wave.set_ydata(new_y)
    f1_line.set_ydata(new_f1)
    f2_line.set_ydata(new_f2)
    return f1_line, f2_line, wave

ani = ani.FuncAnimation(fig, shift, fargs=(dt_plot,), frames=n_frames, interval=30, blit=True)

plt.show()