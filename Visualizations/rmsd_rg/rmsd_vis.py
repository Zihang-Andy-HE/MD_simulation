import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Function to load .xvg files
def load_xvg(file_path):
    data = np.loadtxt(file_path, comments=["#", "@"])
    df = pd.DataFrame(data, columns=["Time (ns)", "RMSD (nm)"])
    return df

# Load RMSD data for initial structures
df_rmsd_280 = load_xvg("/public/home/shenninggroup/zhhe/gromacs/MDfile/rmsd_280.xvg")
df_rmsd_300 = load_xvg("/public/home/shenninggroup/zhhe/gromacs/MDfile/rmsd_300.xvg")
df_rmsd_320 = load_xvg("/public/home/shenninggroup/zhhe/gromacs/MDfile/rmsd_320.xvg")

# Load RMSD data for crystal structures
df_xtal_280 = load_xvg("/public/home/shenninggroup/zhhe/gromacs/MDfile/rmsd_280_xtal.xvg")
df_xtal_300 = load_xvg("/public/home/shenninggroup/zhhe/gromacs/MDfile/rmsd_300_xtal.xvg")
df_xtal_320 = load_xvg("/public/home/shenninggroup/zhhe/gromacs/MDfile/rmsd_320_xtal.xvg")

# Plot RMSD comparison for initial structures
plt.figure(figsize=(10, 6))
plt.plot(df_rmsd_280["Time (ns)"], df_rmsd_280["RMSD (nm)"], label="280 K", color="blue", lw=1.5)
plt.plot(df_rmsd_300["Time (ns)"], df_rmsd_300["RMSD (nm)"], label="300 K", color="green", lw=1.5)
plt.plot(df_rmsd_320["Time (ns)"], df_rmsd_320["RMSD (nm)"], label="320 K", color="red", lw=1.5)
plt.xlabel("Time (ns)", fontsize=12)
plt.ylabel("RMSD (nm)", fontsize=12)
plt.title("RMSD Comparison at Different Temperatures (Initial Structure)", fontsize=14)
plt.legend(frameon=False)
plt.ylim(0, max(df_rmsd_280["RMSD (nm)"].max(), df_rmsd_300["RMSD (nm)"].max(), df_rmsd_320["RMSD (nm)"].max()) + 0.2)
plt.savefig("/public/home/shenninggroup/zhhe/gromacs/rmsd_comparison.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()

# Plot RMSD comparison for crystal structures
plt.figure(figsize=(10, 6))
plt.plot(df_xtal_280["Time (ns)"], df_xtal_280["RMSD (nm)"], label="280 K", color="blue",  lw=1.5)
plt.plot(df_xtal_300["Time (ns)"], df_xtal_300["RMSD (nm)"], label="300 K", color="green",  lw=1.5)
plt.plot(df_xtal_320["Time (ns)"], df_xtal_320["RMSD (nm)"], label="320 K", color="red",  lw=1.5)
plt.xlabel("Time (ns)", fontsize=12)
plt.ylabel("RMSD (nm)", fontsize=12)
plt.title("RMSD Comparison at Different Temperatures (Crystal Structure)", fontsize=14)
plt.legend(frameon=False)
plt.ylim(0, max(df_xtal_280["RMSD (nm)"].max(), df_xtal_300["RMSD (nm)"].max(), df_xtal_320["RMSD (nm)"].max()) + 0.2)
plt.savefig("/public/home/shenninggroup/zhhe/gromacs/rmsd_xtal_comparison.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()

# Calculate and print equilibrium mean RMSD for initial structures
for temp, df in zip([280, 300, 320], [df_rmsd_280, df_rmsd_300, df_rmsd_320]):
    t_start = df["Time (ns)"].max() * 0.5
    mean_rmsd = df[df["Time (ns)"] > t_start]["RMSD (nm)"].mean()
    print(f"Equilibrium mean RMSD at {temp} K (Initial Structure): {mean_rmsd:.3f} nm")

# Calculate and print equilibrium mean RMSD for crystal structures
for temp, df in zip([280, 300, 320], [df_xtal_280, df_xtal_300, df_xtal_320]):
    t_start = df["Time (ns)"].max() * 0.5
    mean_xtal = df[df["Time (ns)"] > t_start]["RMSD (nm)"].mean()
    print(f"Equilibrium mean RMSD at {temp} K (Crystal Structure): {mean_xtal:.3f} nm")