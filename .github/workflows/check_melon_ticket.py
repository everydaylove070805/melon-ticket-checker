import time
import requests
import os

# 設定你的演出、場次、座位 ID
PRODUCT_ID = 210858   # 你的演出 ID
SCHEDULE_ID = 100001  # 你的場次 ID
SEAT_ID = [157, 158, 160, 174, 175, 176, 177, 396, 398, 400, 402, 403, 404, 598, 599, 600, 601, 602, 604, 605, 607, 608, 609, 610, 614, 616, 617, 618, 621, 623, 653, 654, 656, 694, 709, 710, 711, 713, 737, 739, 740, 741, 742]

# 使用環境變數來存帳密（確保密碼不寫在程式碼內）
EMAIL = os.getenv("MELON_EMAIL")  # 在系統環境變數設定 MELON_EMAIL
PASSWORD = os.getenv("MELON_PASSWORD")  # 在系統環境變數設定 MELON_PASSWORD

# LINE Notify 設定
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")  # LINE Token 也用環境變數存
LINE_NOTIFY_URL = "https://notify-api.line.me/api/notify"


def send_line_message(message):
    """ 發送 LINE 通知 """
    headers = {"Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    data = {"message": message}
    response = requests.post(LINE_NOTIFY_URL, headers=headers, data=data)
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.text}")


def login():
    """ 模擬登入 Melon Ticket，回傳 session """
    login_url = "https://ticket.melon.com/login"  # 這個 URL 需要用 F12 確認
    session = requests.Session()

    # 確認帳密是否存在
    if not EMAIL or not PASSWORD:
        print("⚠️ 錯誤：請設定 MELON_EMAIL 和 MELON_PASSWORD 環境變數")
        return None

    login_data = {
        "email": EMAIL,
        "password": PASSWORD,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # 發送登入請求
    response = session.post(login_url, data=login_data, headers=headers)

    if response.status_code == 200:
        print("✅ 登入成功！")
        return session
    else:
        print(f"❌ 登入失敗，狀態碼: {response.status_code}")
        print(f"回應內容: {response.text}")
        return None


def check_ticket(session):
    """ 檢查票務狀態 """
    try:
        CHECK_URL = f"https://ticket.melon.com/api/product/{PRODUCT_ID}/schedule/{SCHEDULE_ID}/seat"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        params = {"seatId": SEAT_ID}  # 用 GET 參數方式傳遞座位 ID

        # 使用 session 來發送請求
        response = session.get(CHECK_URL, headers=headers, params=params)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Content: {response.text}")

        if not response.text:
            print("錯誤：回應內容為空")
            return

        data = response.json()
        available = data.get("available", False)  # 假設 API 返回 {"available": True}

        if available:
            send_line_message("🎟️ 有票了！快去搶票！👉 https://tkglobal.melon.com/performance/index.htm?langCd=EN&prodId=210858")
        else:
            print("❌ 目前沒有票")
    except Exception as e:
        print(f"錯誤：{e}")


if __name__ == "__main__":
    session = login()
    if session:
        while True:
            check_ticket(session)
            time.sleep(5)  # 每 5 秒檢查一次
