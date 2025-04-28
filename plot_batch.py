# pylint: disable=C0114
from config import user, target_mouth
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns


# === 基本設定 ===
#user = '08020020'
#target_mouth = "04"
sheet_name = "Summary"
file_path = rf"D:\LongTermCare\WatchData\{user}\{user}_{target_mouth}month.xlsx"  
print(f"檔案路徑：{file_path}")

# === 讀取資料 ===
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 檢查必要欄位是否存在
required_columns = ['Date', 'Completion rate > 50(%)']
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    raise ValueError(f"缺少必要欄位：{missing_cols}")

# === 繪圖與儲存 ===
# 將時間欄位轉換為 datetime 格式（如果尚未轉換）
df['Date'] = pd.to_datetime(df['Date'])
sns.set_theme(style="darkgrid")
fig, ax = plt.subplots(figsize=(12, 6))  # <-- 用 fig 取代 plt.figure()

# 畫線圖
sns.lineplot(
    data=df,
    x='Date',
    y='Completion rate > 50(%)',
    marker='o',
    linewidth=2,
    color='steelblue',
    ax=ax  # <-- 指定在這個 fig 裡畫
)

# 設定 X軸刻度
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# 設定 Y軸刻度(0-100)
ax.set_ylim(0, 100)

# 資料標籤
for x, y in zip(df['Date'], df['Completion rate > 50(%)']):
    ax.text(x, y + 1, f'{y:.0f}%', ha='center', va='bottom', fontsize=10)

# 警戒線（紅色虛線 50%)與圖例
ax.axhline(50, color='red', linestyle='--', linewidth=1.5, label='50% threshold')
ax.legend(loc='lower right')

# 標題與標籤
ax.set_title(f'{user}_{target_mouth}month_Summary', fontsize=16, fontweight='bold')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Completion Rate (%)', fontsize=12)
plt.xticks(rotation=45)

plt.tight_layout()

# 儲存圖形
save_path = rf"D:\LongTermCare\WatchData\{user}\{user}_{target_mouth}month_Summary_v1.png"
fig.savefig(save_path, dpi=300)
print(f"圖形已儲存至：{save_path}")

plt.show()
plt.close(fig)  # 關閉 fig 避免干擾後續圖表