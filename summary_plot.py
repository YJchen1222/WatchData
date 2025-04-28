# pylint: disable=C0114
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# === 基本設定 ===
excel_path = Path(r"D:\LongTermCare\ProgressReport\0423\group1.xlsx")
output_path = Path(r"D:\LongTermCare\ProgressReport\0430\group1.png")

# 讀取整本 Excel
xls = pd.ExcelFile(excel_path)

# Seaborn 美化樣式
sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)

# 建立一個空的 DataFrame 收集所有人的資料
all_data = pd.DataFrame()

# 遍歷每個 sheet，視為一位 user
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)

    # 確保 Date 是時間格式並排序
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

        # 加一欄 user 名稱
    df['User'] = sheet_name

    # 合併到 all_data
    all_data = pd.concat([all_data, df], ignore_index=True)

# 建立圖表
fig, ax = plt.subplots(figsize=(15, 8))

# 繪製柱狀圖，根據 User 分顏色
sns.barplot(
    data=all_data,
    x='Date',
    y='Completion rate > 50(%)',
    hue='User',        # 這行讓不同使用者分開
    dodge=True,        # 讓同一天的 bar 並排，不要疊在一起
    ax=ax
)

# 設定 Y軸刻度(0-100)
ax.set_ylim(0, 100)

# 添加警戒線（紅色虛線 50%）與圖例
ax.axhline(
    50, color='red',
    linestyle='--',
    linewidth=1.5,
    label='50% threshold'
)

# 圖表外觀設定
ax.set_title(
    'Daily Completion Rate (>50%) per User',
    fontsize=16,
    fontweight='bold'
)
ax.set_xlabel('Date')
ax.set_ylabel('Completion Rate (%)')
ax.tick_params(axis='x', rotation=45)
ax.legend(title="Users")
ax.grid(True)

# 儲存圖形
output_path.parent.mkdir(parents=True, exist_ok=True)  # 確保資料夾存在
plt.tight_layout()
plt.savefig(output_path, dpi=300)
print(f"圖形已儲存至：{output_path}")

# 顯示並關閉圖表
plt.show()
plt.close()
