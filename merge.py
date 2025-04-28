# pylint: disable=C0114
import os
import pandas as pd
from config import user, target_mouth

# 設定你的資料夾路徑
# user = "08020020"
# target_mouth = "04"
folder_path = rf"D:\LongTermCare\WatchData\{user}\file"
output_path = rf"D:\LongTermCare\WatchData\{user}\{user}_{target_mouth}month.xlsx"

# 建立 ExcelWriter 來寫入新的合併檔案
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    for file in os.listdir(folder_path):
        if file.endswith(".xlsx") and file != "merged_results.xlsx":
            file_path = os.path.join(folder_path, file)
            try:
                # 嘗試讀取名為 "Results" 的工作表
                df = pd.read_excel(file_path, sheet_name="Results")

                # 建立工作表名稱（避免超過 Excel 限制）
                sheet_name = os.path.splitext(file)[0][:31]

                # 寫入到新檔案中
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"已加入: {file}")
            except Exception as e:
                print(f"跳過: {file}（原因: {e}）")

print("合併完成！結果儲存在:", output_path)
