import time
import requests
import os
import webbrowser

# 設定你的演出、場次、座位 ID
PRODUCT_ID = 211212   # 你的演出 ID
SCHEDULE_ID = 100001  # 你的場次 ID
SEAT_ID = [157, 158, 160, 174, 175, 176, 177, 396, 398, 400, 402, 403, 404, 598, 599, 600, 601, 602, 604, 605, 607, 608, 609, 610, 614, 616, 617, 618, 621, 623, 653, 654, 656, 694, 709, 710, 711, 713, 737, 739, 740, 741, 742]

# 使用環境變數來存帳密（確保密碼不寫在程式碼內）
EMAIL = os.getenv("secrets.MELON_EMAIL")  # 在系統環境變數設定 MELON_EMAIL
PASSWORD = os.getenv("secrets.MELON_PASSWORD")  # 在系統環境變數設定 MELON_PASSWORD

# LINE Notify 設定
'''LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")  # LINE Token 也用環境變數存
LINE_NOTIFY_URL = "https://notify-api.line.me/api/notify"


def send_line_message(message):
    """ 發送 LINE 通知 """
    headers = {"Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    data = {"message": message}
    response = requests.post(LINE_NOTIFY_URL, headers=headers, data=data)
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.text}")'''

def slackmes(message):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    response = requests.post(webhook_url, json=message)
    
def login():
    """ 模擬登入 Melon Ticket，回傳 session """
    session = requests.Session()

    # 先訪問登入頁面，獲取 CSRF Token 和 Cookie
    login_page_url = "https://ticket.melon.com/login"
    response = session.get(login_page_url)
    
    if response.status_code != 200:
        print(f"❌ 無法訪問登入頁面，狀態碼: {response.status_code}")
        return None

    # 取得 CSRF Token（如果有的話）
    csrf_token = response.cookies.get("XSRF-TOKEN", "")

    login_url = "https://gmember.melon.com/login/login_form.htm?langCd=CN&redirectUrl=https://tkglobal.melon.com/main/index.htm?langCd=CN"  # **請確認這個 API 是否正確**
    
    # 確認帳密是否存在
    if not EMAIL or not PASSWORD:
        print("⚠️ 錯誤：請設定 MELON_EMAIL 和 MELON_PASSWORD 環境變數")
        return None

    login_data = {
        "email": EMAIL,
        "password": PASSWORD,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://ticket.melon.com/",
        "X-XSRF-TOKEN": csrf_token  # 加入 CSRF Token（如果需要）
    }

    # 發送登入請求
    response = session.post(login_url, data=login_data, headers=headers)

    if response.status_code == 200 and "成功" in response.text:  # **請確認回應格式**
        print("✅ 登入成功！")
        return session
    else:
        print(f"❌ 登入失敗，狀態碼: {response.status_code}")
        print(f"回應內容: {response.text}")
        return None


def check_ticket(session):
    """ 檢查票務狀態 """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": f"https://ticket.melon.com/performance/index.htm?langCd=EN&prodId={PRODUCT_ID}"
        }

        for seat_id in SEAT_ID:  # **逐個查詢座位**
            CHECK_URL = f"https://ticket.melon.com/api/product/{PRODUCT_ID}/schedule/{SCHEDULE_ID}/seat/{seat_id}"
            response = session.get(CHECK_URL, headers=headers)

            print(f"🎫 查詢座位 {seat_id}，狀態碼: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Content: {response.text}")

            if response.status_code == 200:
                data = response.json()
                available = data.get("available", False)  # 假設 API 返回 {"available": True}

                if available:
                    slackmes(f"🎟️ 座位 {seat_id} 有票了！快去搶票！👉 https://tkglobal.melon.com/performance/index.htm?langCd=EN&prodId={PRODUCT_ID}")
                    webbrowser.open("https://www.bilibili.com")
                    seat = response.find_element(By.CSS_SELECTOR, f".seat[data-seat-id='{seat_id}']")
                    seat.click()
                    print(f"✅ 成功选中座位 {seat_id}")
                    confirm_button = response.find_element(By.CSS_SELECTOR, ".btn-confirm")
                    confirm_button.click()
                    print("✅ 已提交选座！")
                #    send_line_message(f"🎟️ 座位 {seat_id} 有票了！快去搶票！👉 https://tkglobal.melon.com/performance/index.htm?langCd=EN&prodId={PRODUCT_ID}")
            elif response.status_code == 404:
                print(f"⚠️ 座位 {seat_id} 無效或查無資料")
            elif response.status_code == 406:
                print(f"🚫 請求被拒，可能需要修改 headers")
            else:
                print(f"⚠️ 未知錯誤：{response.status_code}")
            time.sleep(1)  # 避免請求太頻繁

    except Exception as e:
        print(f"❌ 錯誤：{e}")


if __name__ == "__main__":
    session = login()
    if session:
        while True:
            check_ticket(session)
            time.sleep(5)  # 每 5 秒檢查一次
