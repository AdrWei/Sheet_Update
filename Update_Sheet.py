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
        sheet = spreadsheet.worksheet("orderWeb")
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title="orderWeb", rows=100, cols=20)
    existing_web_data = sheet.get_all_values()
    existing_web_df = pd.DataFrame(existing_web_data[1:], columns=existing_web_data[0])
    if not existing_web_df.empty:
        existing_web_df.iloc[:, :len(df_web.columns)] = df_web.values
    else:
        existing_web_df = df_web
    sheet.clear()
    sheet.update([existing_web_df.columns.values.tolist()] + existing_web_df.values.tolist())

    # 处理 orderSocial 工作表
    try:
        sheet = spreadsheet.worksheet("orderSocial")
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title="orderSocial", rows=100, cols=20)
    existing_social_data = sheet.get_all_values()
    existing_social_df = pd.DataFrame(existing_social_data[1:], columns=existing_social_data[0])
    if not existing_social_df.empty:
        existing_social_df.iloc[:, :len(df_social.columns)] = df_social.values
    else:
        existing_social_df = df_social
    sheet.clear()
    sheet.update([existing_social_df.columns.values.tolist()] + existing_social_df.values.tolist())

    print("数据成功写入 Google Sheet！")
except gspread.exceptions.SpreadsheetNotFound as e:
    print(f"Error: Google Sheet not found. Please check the SHEET_ID.")
    raise
except Exception as e:
    print(f"Error: {e}")
    raise
