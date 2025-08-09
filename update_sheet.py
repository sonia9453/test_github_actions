from datetime import datetime
import os
import json
import gspread
from google.oauth2.service_account import Credentials

def main():
    # 讀取 Google Sheets API 憑證
    # GOOGLE_SHEETS_CREDENTIALS 是一個機密資訊，請在 GitHub Repo 的 Settings > Secrets 中設為機密環境變數（應是完整 JSON 內容）。
    creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
    if not creds_json:
        raise ValueError("找不到 GOOGLE_SHEETS_CREDENTIALS 環境變數")

    try:
        creds_dict = json.loads(creds_json)
    except json.JSONDecodeError:
        raise ValueError("GOOGLE_SHEETS_CREDENTIALS 格式錯誤，無法解析 JSON")

    # 設定授權範圍並建立憑證
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

    # 連線到 Google Sheets
    gc = gspread.authorize(creds)

    # 指定要操作的 Google Sheet（請替換 SHEET_ID）
    SHEET_ID = "YOUR_SHEET_ID"  # ⚠️ 請替換成你的實際 Sheet ID
    try:
        # .sheet1 是 gspread 的快捷方式，用來取得該 Google 試算表中第一個工作表（worksheet）。
        worksheet = gc.open_by_key(SHEET_ID).sheet1
    except Exception as e:
        raise RuntimeError(f"無法開啟工作表：{e}")

    # 寫入目前時間和訊息
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row([now, "GitHub Actions 自動記錄"])
    print(f"✅ 已成功寫入：{now}")

# 在 Python 中，每個檔案（模組）都有一個內建變數叫做 __name__。
# 如果你是 直接執行這個檔案（例如：python update_sheet.py），那 __name__ 的值就是 "__main__"，所以 main() 會被執行。
# 如果你是從別的 Python 檔案引用這個檔案（像是 import update_sheet），那 __name__ 的值就會是 "update_sheet"，main() 就不會被自動執行。
if __name__ == "__main__":
    main()
