# pylint: disable=C0114
import re
from datetime import datetime, timedelta


# === 自動更新 config.py 中的 target_date ===
def update_target_date_in_config():

    """
    在plot.py後，自動將config.py中的target_date變數增加一天"""

    config_path = 'config.py'

    # 讀取 config.py 文件
    with open(config_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 使用正規表達式查找 target_date 變數並提取日期
    date_pattern = r'target_date\s*=\s*"(\d{4}-\d{2}-\d{2})"'
    match = re.search(date_pattern, content)
    
    if match:
        current_date_str = match.group(1)
        # 將字符串轉換為日期對象
        current_date = datetime.strptime(current_date_str, '%Y-%m-%d')
        # 日期加一天
        next_date = current_date + timedelta(days=1)
        # 轉換回字符串格式
        next_date_str = next_date.strftime('%Y-%m-%d')
        
        # 替換舊日期為新日期
        updated_content = re.sub(
            date_pattern,
            f'target_date = "{next_date_str}"', content)
        
        # 寫回文件
        with open(config_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
            
        print(f"\n✅ config.py 中的日期已從 {current_date_str} 更新至 {next_date_str}")
    else:
        print("\n❌ 在 config.py 中未找到 target_date 變數")
        return False

# 只有在直接運行此文件時才執行
if __name__ == "__main__":
    # 在程式結束前執行更新 config.py 的函數
    update_target_date_in_config()