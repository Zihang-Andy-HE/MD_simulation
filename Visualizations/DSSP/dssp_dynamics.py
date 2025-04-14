import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Function to load .xvg files
def load_ss_xvg(file_path):
    data = np.loadtxt(file_path, comments=["#", "@"])
    df = pd.DataFrame(data, columns=["Time (ps)", "Loops", "Breaks","Bends","Turns","PP_Helices","π-Helices","3⏨-Helices","β-Strands","β-Bridges","α-Helices"])
    return df

df_ss_280 = load_ss_xvg("/path/dssp_280.xvg")
df_ss_300 = load_ss_xvg("/path/dssp_300.xvg")
df_ss_320 = load_ss_xvg("/path/dssp_320.xvg")

# 配置参数
structures = ['α-Helices', 'β-Strands', 'β-Bridges']
colors = {'α-Helices': '#E63946', 
          'β-Strands': '#1D3557', 
          'β-Bridges': '#2A9D8F'}  # 使用高对比度的科学配色
linestyle = '-'  # 统一线型

# 创建三个独立图表
for temp in ['280', '300', '320']:
    plt.figure(figsize=(10, 6), dpi=150)
    df = globals()[f'df_ss_{temp}']
    
    # 绘制三条曲线
    for ss in structures:
        plt.plot(df['Time (ps)'], df[ss], 
                 color=colors[ss], 
                 linestyle=linestyle,
                 linewidth=2.5,
                #  marker='o',          #
                #  markersize=4,
                 label=ss)
    
    
    plt.title(f'Secondary Structure Dynamics ({temp}K)', fontsize=14, pad=20)
    plt.xlabel('Time (ps)', fontsize=12, labelpad=10)
    plt.ylabel('Residue Count', fontsize=12, labelpad=10)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), 
               ncol=3, frameon=False)  
    
    # Set axis
    plt.xlim(0, df['Time (ps)'].max())
    plt.ylim(0, df[structures].max().max()*1.1)
    plt.xticks(np.arange(0, 50001, 10000))  
    plt.grid(True, linestyle=':', alpha=0.5)  
    
    # Save Figure
    plt.tight_layout()
    plt.savefig(f'/path/secondary_structure_{temp}K.png', 
                bbox_inches='tight', dpi=300)
    plt.close()

