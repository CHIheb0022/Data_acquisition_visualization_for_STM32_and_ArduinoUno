from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

plt.rcParams["figure.figsize"] = (12, 4)

N = 2 ** 10
lwL = 2
axRxlims = [0, N]
axRylims = [0, 160]

_t = np.linspace(0, N, N)
_y = 1 + np.sin((5 / N) * 2 * np.pi * _t)

dframe = np.full(N + 1, fill_value=np.nan, dtype=float)  # Use float directly

t = np.tile(_t, (N, 1))
y = np.tile(_y, (N, 1))

for i in range(N):
    t[i, i + 1:] = np.nan
    y[i, i + 1:] = np.nan

fig, axL = plt.subplots(figsize=(6, 4), tight_layout=True)

def getfigax():
    linel, = axL.plot([], [], lw=lwL, label='Left Line')
    titl = axL.set_title('Left Plot Title')

    axL.set_xlabel("distance")
    axL.set_ylabel("Terrain Height (m)")
    axL.grid(True)


    return (fig, axL, titl, linel)

def update(frame, frame_times):
    
    frame_times[frame] = time.perf_counter()
    linel.set_data(t[frame], y[frame])
    titl.set_text(f"Frame: {N - frame}")
    
    rescale = False
    if y[frame, frame] < axL.get_ylim()[0]:
        axL.set_ylim(y[frame, frame] - 0.1, axL.get_ylim()[1])
        rescale = True
    if y[frame, frame] > axL.get_ylim()[1]:
        axL.set_ylim(axL.get_ylim()[0], y[frame, frame] + 0.1)
        rescale = True
    if t[frame, frame] > axL.get_xlim()[1]:
        axL.set_xlim(axL.get_xlim()[0], axL.get_xlim()[1] + N / 5)
        rescale = True
    if frame == len(t) - 1:
        rescale = True
    
    if rescale:
        fig.canvas.draw()
    
    return linel, titl

fig, axL, titl, linel = getfigax()
fig.suptitle("Func Animation: Blitting Intelligent ax update")
frame_times = np.zeros(N)
ani = FuncAnimation(fig, update, interval=0, fargs=(frame_times,), repeat=False, frames=list(range(N)), blit=True)

plt.show()
