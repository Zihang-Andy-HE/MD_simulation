import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import f_oneway

df=pd.read_csv("/path/no_salt_bridge.csv")
# Preprocess convert to long format
df_long = df.melt(var_name='Group', value_name='Value')

plt.figure(figsize=(10, 6))
ax = sns.violinplot(x='Group', y='Value', data=df_long, inner='box', color='lightblue')
sns.stripplot(x='Group', y='Value', data=df_long, color='black', size=4, jitter=True)

# ANOVA + Tukey
groups = [df[col].values for col in df.columns]
f_stat, p_value = f_oneway(*groups)
print(f"ANOVA Result: F = {f_stat:.2f}, p = {p_value:.8f}")
def get_star(p):
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    
significant_pairs = []
if p_value < 0.05:
    tukey = pairwise_tukeyhsd(endog=df_long['Value'], groups=df_long['Group'], alpha=0.05)
    print(tukey)
    # 提取显著差异组对
    for res in tukey.summary().data[1:]:
        g1, g2, _, _, p_adj, reject = res[0], res[1], res[2], res[3], res[5], res[6]
        if reject:
            significant_pairs.append((g1, g2))


xticks = ax.get_xticks()                       # array([0,1,2,...])
xticklabels = [t.get_text() for t in ax.get_xticklabels()]
pos = dict(zip(xticklabels, xticks))           # {'A':0, 'B':1, 'C':2, ...}
max_value = df_long['Value'].max()
y_offset = max_value * 0.05  # Vertical offset

for i, (g1, g2) in enumerate(significant_pairs):
    x1, x2 = pos[g1], pos[g2]
    y = max_value + y_offset * (i + 1)
    ax.plot([x1, x2], [y, y], lw=1, color='black')
    ax.text((x1 + x2) / 2, y, get_star(p_value), ha='center', va='bottom', fontsize=8, color='black')


plt.title('Comparison of Salt Bridges Number')
plt.xlabel('Group')
plt.ylabel('NSB')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("/path/no_salt_bridge_violin.png", dpi=300, bbox_inches='tight')
plt.show()
