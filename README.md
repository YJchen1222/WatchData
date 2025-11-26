# WatchData

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)

## 📝 專案介紹 (Introduction)

`WatchData` 是一個基於 Python 的工具，專門用於**自動化處理從穿戴式設備集到的數據**。

本專案的核心功能包括數據的批量合併、格式化處理以及生成數據視覺化圖表，旨在幫助研究人員或用戶更高效地管理和分析時間序列數據。

## ✨ 主要功能 (Features)

* **數據批量合併：** 自動將位於指定目錄下的多個 Excel/CSV 檔案進行合併（透過 `excel_merge.py` 或 `merge.py`）。
* **批量圖表生成：** 能夠對多組數據執行批量視覺化處理，生成趨勢圖或其他分析圖表（透過 `plot_batch.py`）。
* **資料視覺化：** 針對特定指標生成彙總圖表，提供數據概覽（透過 `summary_plot.py`）。
* **配置化管理：** 透過 `config.py` 檔案輕鬆管理數據路徑、參數和設定。
* **自動更新日期：** 包含實用的日期和時間處理工具（透過 `date_utils.py`）。

## 🛠️ 技術堆棧 (Tech Stack)

**主要語言:**
* Python (100%)

**推測使用的函式庫:**
* **數據處理:** `[Pandas]`
* **數據視覺化:** `[Matplotlib]` 或 `[Seaborn]`
* **Excel 處理:** `[openpyxl]` 或 `[xlrd]` (用於讀寫 Excel 文件)
