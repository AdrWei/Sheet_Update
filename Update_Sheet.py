import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri

# 创建 orderWeb 工作表的数据
data_web = {
    "Order ID": [101, 102, 103],
    "Product": ["Laptop", "Phone", "Tablet"],
    "Quantity": [1, 2, 1],
    "Price": [1200, 800, 500]
}

# 创建 orderSocial 工作表的数据
data_social = {
    "Order ID": [201, 202, 203],
    "Platform": ["Instagram", "Facebook", "Twitter"],
    "Clicks": [150, 200, 100],
    "Conversions": [10, 15, 8]
}

# 将数据转换为 DataFrame
df_web = pd.DataFrame(data_web)
df_social = pd.DataFrame(data_social)

# 设置 Google Sheets API 的权限范围
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 从环境变量中获取服务账号 JSON 和 Google Sheet ID
json_key = "credentials.json"  # 将 JSON 密钥文件写入本地文件
sheet_id = os.getenv("SHEET_ID")  # 从环境变量中获取 Google Sheet ID

# 加载服务账号的 JSON 密钥文件
creds = ServiceAccountCredentials.from_json_keyfile_name(json_key, scope)
client = gspread.authorize(creds)

# 打开 Google Sheet
try:
    # 获取 Google Sheet
    spreadsheet = client.open_by_key(sheet_id)

    # 处理 orderWeb 工作表
    try:
        sheet = spreadsheet.worksheet("orderWeb")  # 尝试获取名为 "orderWeb" 的工作表
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title="orderWeb", rows=100, cols=20)  # 如果不存在，创建新工作表

    # 读取现有数据
    existing_data = sheet.get_all_values()
    existing_df = pd.DataFrame(existing_data[1:], columns=existing_data[0])

    # 用新的 DataFrame 更新前四列
    if not existing_df.empty:  # 确保 Google Sheet 中有数据
        existing_df.iloc[:, :len(df_web.columns)] = df_web.values  # 更新前四列
    else:  # 如果 Google Sheet 为空，则直接写入新的 DataFrame
        existing_df = df_web

    # 清空并写入更新后的数据
    sheet.clear()
    sheet.update([existing_df.columns.values.tolist()] + existing_df.values.tolist())

    # 处理 orderSocial 工作表（保持不变）
    try:
        sheet = spreadsheet.worksheet("orderSocial")  # 尝试获取名为 "orderSocial" 的工作表
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title="orderSocial", rows=100, cols=20)  # 如果不存在，创建新工作表
    sheet.clear()  # 清空现有数据
    sheet.update([df_social.columns.values.tolist()] + df_social.values.tolist())  # 写入表头和数据

    print("数据成功写入 Google Sheet！")
except gspread.exceptions.SpreadsheetNotFound as e:
    print(f"Error: Google Sheet not found. Please check the SHEET_ID.")
    raise
except Exception as e:
    print(f"Error: {e}")
    raise
