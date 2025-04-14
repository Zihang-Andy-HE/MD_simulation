import matplotlib.pyplot as plt
import numpy as np

def load_xvg(file):
    data = np.loadtxt(file, comments=['#','@'])
    return data[:,0], data[:,1]

time_280, rg_280 = load_xvg('/public/home/shenninggroup/zhhe/gromacs/MDfile/gyrate_280.xvg')
time_300, rg_300 = load_xvg('/public/home/shenninggroup/zhhe/gromacs/MDfile/gyrate_300.xvg')
time_320, rg_320 = load_xvg('/public/home/shenninggroup/zhhe/gromacs/MDfile/gyrate_320.xvg')

plt.plot(time_280, rg_280, label='280K', color="blue", lw=1.5)
plt.plot(time_300, rg_300, label='300K', color="green", lw=1.5)
plt.plot(time_320, rg_320, label='320K', color="red", lw=1.5)
plt.xlabel('Time (ps)')
plt.ylabel('Rg (nm)')
plt.legend()
plt.title("Comparison of Radius of Gyration (Rg) under Different Temperatures")
plt.savefig('/public/home/shenninggroup/zhhe/gromacs/rg_comparison.png', dpi=300)

