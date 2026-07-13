import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置学术论文风格的绘图参数
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)

def plot_distribution_analysis(df, output_path="data/raw/figure1_distribution.png"):
    """
    绘制双子图：左边展示高频密集区(1x-10x)，右边用对数坐标展示完整的长尾分布
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # 图 A：1x-10x 核心区直方图
    core_data = df[df['crash_point'] <= 10]['crash_point']
    sns.histplot(core_data, bins=40, kde=True, color='#1f77b4', ax=ax1, stat="proportion")
    ax1.set_title("A: Probability Density of Core Multipliers (1x - 10x)", fontsize=13, fontweight='bold', pad=12)
    ax1.set_xlabel("Crash Multiplier (x)")
    ax1.set_ylabel("Proportion of Total Rounds")

    # 标注中位数和均值（核心区）
    median_val = df['crash_point'].median()
    mean_val = df['crash_point'].mean()
    ax1.axvline(median_val, color='#d62728', linestyle='--', linewidth=1.5, label=f'Median: {median_val:.2f}x')
    ax1.legend(loc='upper right')

    # 图 B：全量数据对数坐标图（展示 Heavy-Tailed 特征）
    sns.histplot(df['crash_point'], bins=100, color='#2ca02c', ax=ax2, stat="count", log_scale=(True, True))
    ax2.set_title("B: Global Tail Distribution (Log-Log Scale)", fontsize=13, fontweight='bold', pad=12)
    ax2.set_xlabel("Crash Multiplier (Log Scale x)")
    ax2.set_ylabel("Frequency Count (Log Scale)")

    # 标注全局均值
    ax2.axvline(mean_val, color='#ff7f0e', linestyle='-', linewidth=1.5, label=f'Global Mean: {mean_val:.4f}x')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[成功] 分布分析图已保存至: {output_path}")

def plot_timeseries_analysis(df, output_path="data/raw/figure2_timeseries.png"):
    """
    绘制前 100 轮的时序演变图，展示 crash_point 的随机独立性，以及 rolling_mean 和 rolling_std 的表现
    """
    # 截取前 100 轮进行可视化
    subset = df.head(100).copy()

    plt.figure(figsize=(14, 6))

    # 1. 绘制真实观测值（散点+淡细线，强调独立不连续）
    plt.plot(subset['round_id'], subset['crash_point'], color='#7f7f7f', alpha=0.3, linestyle='-', linewidth=1)
    plt.scatter(subset['round_id'], subset['crash_point'], color='#1f77b4', s=25, alpha=0.8, label='Actual Crash Point ($X_t$)')

    # 2. 绘制 20 轮滚动均值（展示由于大数导致的滞后跳跃）
    plt.plot(subset['round_id'], subset['rolling_mean_20'], color='#e377c2', linewidth=2, label='Rolling Mean (Window=20)')

    # 3. 填充滚动标准差区域（展示局部波动范围，浅色阴影）
    # 为了防止负值，下界与 1.0 取最大值
    lower_bound = np.maximum(subset['rolling_mean_20'] - subset['rolling_std_20'], 1.0)
    upper_bound = subset['rolling_mean_20'] + subset['rolling_std_20']
    plt.fill_between(subset['round_id'], lower_bound, upper_bound, color='#e377c2', alpha=0.15, label='Rolling Volatility Interval ($\pm 1\sigma$)')

    # 图表细节美化
    plt.title("Time-Series Realization & 20-Round Rolling Metrics (First 100 Rounds)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Sequential Round Identifier ($t$)")
    plt.ylabel("Multiplier Value (x)")
    plt.xlim(-2, 102)

    # 突出展示前 20 轮的 Burn-in（热身）无特征阶段
    plt.axvspan(-2, 19, color='#bcbd22', alpha=0.08, label='Burn-in Phase (NaN Features)')

    plt.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='none')
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[成功] 时序分析图已保存至: {output_path}")

# ==========================================
# 执行示范（假设您已经运行了上一轮修正后的 generate_dataset 函数）
# ==========================================
if __name__ == "__main__":
    # 注意：为了让绘图脚本直接演示，此处临时读取数据。
    # 实际应用中，您只需在 generate_dataset(1000000) 执行完毕返回 df 后，直接调用这两个绘图函数即可。
    csv_path = "data/raw/crash_dataset.csv"

    if os.path.exists(csv_path):
        print("正在读取数据集并生成学术图表...")
        # 针对 100 万行的大数据，读取前 50000 行足够绘制完美的总体分布，节约内存
        df_sample = pd.read_csv(csv_path, nrows=50000)

        plot_distribution_analysis(df_sample)
        plot_timeseries_analysis(df_sample)
    else:
        print(f"[错误] 未找到数据集文件 '{csv_path}'。请先运行数据集生成脚本！")
