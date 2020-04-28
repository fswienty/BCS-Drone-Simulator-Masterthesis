import sys
import numpy as np
import matplotlib.pyplot as plt


x = [0, 10, 20, 40, 60, 80, 100, 120]
dataRaw = np.load(sys.path[0] + "/complete_results.npy")
data = dataRaw[:,1,:]

y = np.mean(data, axis=1)
std = np.std(data, axis=1)

fig, ax = plt.subplots()
plt.ylim(ymin = 0, ymax = 1)
ax.bar(x, y,
       yerr=std,
       align='center',
       color=('#ff7f0e'),
       ecolor='black',
       width=7,
       capsize=10)

ax.set_xlabel('Timeslot length (ms)')
ax.set_ylabel('Trajectory efficiency')
ax.set_xticks(x)
ax.yaxis.grid(True)

SAVE = True
if SAVE:
    plt.savefig(sys.path[0] + "/eff4.pdf", dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False, bbox_inches='tight', pad_inches=0,
                frameon=None, metadata=None)
else:
    plt.show()
