# pylint: disable=C0114
from config import user, target_date, location
from date_utils import update_target_date_in_config
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns

# === 基本設定 ===
#user = "08020020"
#target_date = "2025-04-07"
sheet_name = "Results"
file_path = rf"D:\LongTermCare\WatchData\{location}\{user}\file\{target_date}_30mins.xlsx"

print(f"檔案路徑：{file_path}")

# === 讀取資料 ===
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 檢查必要欄位是否存在
required_columns = ['30mins_interval', 'Completion rate(%)']
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    raise ValueError(f"缺少必要欄位：{missing_cols}")

# === 繪圖與儲存 ===
# 將時間欄位轉換為 datetime 格式（如果尚未轉換）
df['30mins_interval'] = pd.to_datetime(df['30mins_interval'])
sns.set_theme(style="darkgrid")
fig, ax = plt.subplots(figsize=(12, 6))  # <-- 用 fig 取代 plt.figure()

# 畫線圖
sns.lineplot(
    data=df,
    x='30mins_interval',
    y='Completion rate(%)',
    marker='o',
    linewidth=2,
    color='steelblue',
    ax=ax  # <-- 指定在這個 fig 裡畫
)

# 設定 X 軸刻度
start_time = df['30mins_interval'].min().replace(minute=0, second=0)
end_time = df['30mins_interval'].max() + pd.Timedelta(minutes=30)
ax.set_xlim(start_time, end_time)
ax.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 30]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# 設定 Y軸刻度(0-100)
ax.set_ylim(0, 100)

# 警戒線（紅色虛線 50%)與圖例
ax.axhline(50, color='red', linestyle='--', linewidth=1.5, label='50% threshold')
ax.legend(loc='lower right')

# 標題與標籤
ax.set_title(f'{user}_{target_date}_Completion rate', fontsize=16, fontweight='bold')
ax.set_xlabel('Time', fontsize=12)
ax.set_ylabel('Completion Rate (%)', fontsize=12)
plt.xticks(rotation=45)

plt.tight_layout()

# 儲存圖形
save_path = rf"D:\LongTermCare\WatchData\{location}\{user}\fig\{user}_{target_date}_Completion rate(%).png"
fig.savefig(save_path, dpi=300)
print(f"圖形已儲存至：{save_path}")

plt.close(fig)  # 關閉 fig 避免干擾後續圖表

# 更新config.py中的日期
update_target_date_in_config()
