# pylint: disable=C0114
from config import user, target_date, location
import pandas as pd
# === 基本設定 ===
# user = '08020020'
# target_date = "2025-04-12"
sheet_name = "心率.脈搏"
file_path = rf"D:\LongTermCare\WatchData\{location}\{user}\20250513162411r.xlsx"


print(f"檔案路徑：{file_path}")
print(f"工作表名稱：{sheet_name}")
print(f"在main.py程式運行中: 用戶是 {user}, 目標日期是 {target_date}")

# === 讀取資料 ===
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 檢查必要欄位是否存在
required_columns = ['時間', '量測值']
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    raise ValueError(f"缺少必要欄位：{missing_cols}")

# 時間欄位轉換與清洗
df['時間'] = pd.to_datetime(df['時間'], errors='coerce')
df.dropna(subset=['時間'], inplace=True)  # 刪除無效時間

# 篩選整天的資料
# 使用 .copy() 避免警告
date_obj = pd.to_datetime(target_date).date()
day_df = df[df['時間'].dt.date == date_obj].copy()

# === 區間統計 ===
interval_label = '30mins_interval'
day_df[interval_label] = day_df['時間'].dt.floor('30min')

# 建立完整的 30 分鐘時間序列
full_intervals = pd.date_range(
    start=f"{target_date} 00:00:00",
    end=f"{target_date} 23:30:00",  # 固定在整天的最後半小時
    freq='30min'
).to_frame(index=False, name=interval_label)

# 統計實際有資料的區間
actual_counts = (
    day_df.groupby(interval_label)
    .size()
    .reset_index(name='Detections')
)

# 合併完整區間與實際統計，補上缺值為 0
interval_counts = pd.merge(
    full_intervals, 
    actual_counts, 
    on=interval_label, 
    how='left')

interval_counts['Detections'] = interval_counts['Detections'].fillna(0).astype(int)

# 加入理論筆數與完整率
interval_counts['Theory'] = 30  # 每個 30 分鐘區間理論上應有 30 筆資料
interval_counts['Completion rate(%)'] = (
    interval_counts['Detections'] / interval_counts['Theory']) * 100

# 顯示統計結果
print(f"📅 {target_date} 的 30 分鐘區間資料覆蓋：")
print(interval_counts)

# === 缺失區間檢查 ===
full_intervals = pd.date_range(
    start=f"{target_date} 00:00:00",
    end=f"{target_date} 23:59:59",
    freq='30min'
)
existing_intervals = day_df[interval_label].dropna().unique()
missing_intervals = full_intervals[~full_intervals.isin(existing_intervals)]
missing_df = pd.DataFrame({'Loss_intervals': missing_intervals})

# 顯示缺失區間
print("\n🕳️ 缺失的 30 分鐘區間：")
if len(missing_intervals) == 0:
    print("✔️ 沒有缺失區間")
else:
    for t in missing_intervals:
        print(f" - {t.strftime('%y/%m/%d %H:%M')}")

#  總筆數檢查(是否超過 720 筆)
record_count = len(day_df)
print(f"📅{target_date} 天共有 {record_count} 筆資料")
if record_count >= 720:
    print("✅ 總筆數達標（≥ 720）")
else:
    print("⚠️ 總筆數不足（< 720）")

# 匯出成 Excel
interval_counts[interval_label] = pd.to_datetime(interval_counts[interval_label]).dt.strftime('%Y-%m-%d %H:%M:%S')
missing_df['Loss_intervals'] = missing_df['Loss_intervals'].dt.strftime('%Y-%m-%d %H:%M:%S')

# current_time = datetime.now().strftime('%Y%m%d%H%M%S')
output_path = rf"D:\LongTermCare\WatchData\{location}\{user}\file\{target_date}_30mins.xlsx"
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    interval_counts.to_excel(writer, sheet_name='Results', index=False)
    missing_df.to_excel(writer, sheet_name='Loss_intervals', index=False)

print(f"\n✅ 結果已匯出至：{output_path}")
