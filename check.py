from config import user, target_mouth, location
import pandas as pd

# 讀取 Excel 檔案
sheet_name = "Summary"
file_path = rf"D:\LongTermCare\WatchData\{location}\{user}\{user}_{target_mouth}month.xlsx"

df = pd.read_excel(file_path, sheet_name=sheet_name)

# 將欄位名稱標準化，避免空白或特殊符號造成問題
df.columns = [col.strip() for col in df.columns]

# 篩選出 Completion rate > 50(%) > 50 的行
filtered_df = df[df["Completion rate > 50(%)"] > 50]

# 印出符合條件的日期
print("Completion rate > 50 的日期：")
print(filtered_df["Date"])

# 印出符合條件的總天數
print(f"\n共有 {len(filtered_df)} 天的 Completion rate > 50。")
