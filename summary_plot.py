# pylint: disable=C0114
import pandas as pd
import plotly.express as px
from pathlib import Path

# === 基本設定 ===
excel_path = Path(r"D:\LongTermCare\ProgressReport\0423\group1.xlsx")
output_path = Path(r"D:\LongTermCare\ProgressReport\0430\group1_plotly.html")

# 讀取整本 Excel
xls = pd.ExcelFile(excel_path)

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

# 使用 plotly express 畫動態柱狀圖
fig = px.bar(
    all_data,
    x='Date',
    y='Completion rate > 50(%)',
    color='User',  # 分色
    barmode='group',  # 同一天多個 user 的柱子並排
    title='Daily Completion Rate (>50%) per User',
    labels={
        'Date': 'Date',
        'Completion rate > 50(%)': 'Completion Rate (%)'
    },
    hover_data=['User', 'Completion rate > 50(%)']
)

# 加上 50% 警戒線
fig.add_shape(
    type='line',
    x0=all_data['Date'].min(), x1=all_data['Date'].max(),
    y0=50, y1=50,
    line=dict(color='red', dash='dash', width=2),
)

# 更新 layout
fig.update_layout(
    yaxis=dict(range=[0, 100]),
    xaxis_title='Date',
    yaxis_title='Completion Rate (%)',
    legend_title_text='Users',
    bargap=0.2,
)

# 儲存成 HTML（可以雙擊打開看，或上傳網頁）
output_path.parent.mkdir(parents=True, exist_ok=True)
fig.write_html(str(output_path))
print(f"互動式圖表已儲存至：{output_path}")

# 顯示圖表
fig.show()
