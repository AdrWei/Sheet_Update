library(googlesheets4)
library(dplyr)

# 创建 orderWeb 工作表的数据
data_web <- data.frame(
  `Order ID` = c(101, 102, 103),
  Product = c("Laptop", "Phone", "Tablet"),
  Quantity = c(1, 2, 1),
  Price = c(1200, 800, 500)
)

# 创建 orderSocial 工作表的数据
data_social <- data.frame(
  `Order ID` = c(201, 202, 203),
  Platform = c("Instagram", "Facebook", "Twitter"),
  Clicks = c(150, 200, 100),
  Conversions = c(10, 15, 8)
)

# 设置 Google Sheets API 的权限范围
gs4_auth(path = "credentials.json")  # 加载服务账号的 JSON 密钥文件

# 从环境变量中获取 Google Sheet ID
sheet_id <- Sys.getenv("SHEET_ID")

# 打开 Google Sheet
tryCatch({
  # 获取 Google Sheet
  spreadsheet <- gs4_get(sheet_id)

  # 处理 orderWeb 工作表
  if ("orderWeb" %in% sheet_names(spreadsheet)) {
    # 如果工作表存在，读取现有数据
    existing_web_data <- read_sheet(spreadsheet, sheet = "orderWeb")
    # 合并新数据和现有数据
    updated_web_data <- bind_rows(existing_web_data, data_web)
  } else {
    # 如果工作表不存在，创建新工作表
    updated_web_data <- data_web
    sheet_add(spreadsheet, sheet = "orderWeb", .before = 1)
  }
  # 更新 orderWeb 工作表
  write_sheet(updated_web_data, spreadsheet, sheet = "orderWeb")

  # 处理 orderSocial 工作表
  if ("orderSocial" %in% sheet_names(spreadsheet)) {
    # 如果工作表存在，读取现有数据
    existing_social_data <- read_sheet(spreadsheet, sheet = "orderSocial")
    # 合并新数据和现有数据
    updated_social_data <- bind_rows(existing_social_data, data_social)
  } else {
    # 如果工作表不存在，创建新工作表
    updated_social_data <- data_social
    sheet_add(spreadsheet, sheet = "orderSocial", .before = 2)
  }
  # 更新 orderSocial 工作表
  write_sheet(updated_social_data, spreadsheet, sheet = "orderSocial")

  print("数据成功写入 Google Sheet！")
}, error = function(e) {
  print(paste("Error:", e$message))
  stop(e)
})
