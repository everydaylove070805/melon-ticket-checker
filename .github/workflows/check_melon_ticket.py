import time
import requests

# 設定你的演出、場次、座位 ID
PRODUCT_ID = 210858   # 你的演出 ID
SCHEDULE_ID = 100001  # 你的場次 ID
SEAT_ID_LIST = [157, 158, 160, 174, 175, 176, 177, 396, 398, 400, 402, 403, 404, 598, 599, 600, 601, 602, 604, 605, 607, 608, 609, 610, 614, 616, 617, 618, 621, 623, 653, 654, 656, 694, 709, 710, 711, 713, 737, 739, 740, 741, 742]  # 座位 ID
SEAT_ID_STR = ",".join(map(str, SEAT_ID_LIST))  # 轉換成逗號分隔字串

# LINE Notify 設定
LINE_ACCESS_TOKEN = "93FXd8FB5ziW5Vo8WXnjfjakytxzEQL7gZU4jCZDwmo"
LINE_NOTIFY_URL = "https://notify-api.line.me/api/notify"


def send_line_message(message):
    """ 發送 LINE 通知 """
    headers = {"Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    data = {"message": message}
    response = requests.post(LINE_NOTIFY_URL, headers=headers, data=data)

    # 檢查回應狀態和內容
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.text}")


def check_ticket():
    """ 檢查票務狀態 """
    try:
        CHECK_URL = f"https://ticket.melon.com/api/product/{PRODUCT_ID}/schedule/{SCHEDULE_ID}/seat/{SEAT_ID_STR}"

        # 設定 headers，增加 Accept 和 Referer
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://ticket.melon.com/"
        }

        # 使用 requests.Session() 來維持連線
        session = requests.Session()
        session.headers.update(headers)

        # 發送請求
        response = session.get(CHECK_URL)

        # 打印回應狀態碼和回應內容
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Content: {response.text}")

        # 如果回應為空或格式不正確，則輸出提示並返回
        if not response.text:
            print("錯誤：回應內容為空")
            return

        # 嘗試解析 JSON 資料
        try:
            data = response.json()
        except requests.JSONDecodeError:
            print("❌ 錯誤：無法解析 JSON，可能是 API 回應格式變更")
            return

        # 確保 API 返回的資料格式正確
        available = data.get("available", False)  # 假設 API 返回 {"available": True}

        if available:
            send_line_message("🎟️ 有票了！快去搶票！👉 https://tkglobal.melon.com/performance/index.htm?langCd=EN&prodId=210858")
        else:
            print("❌ 目前沒有票")

    except requests.RequestException as e:
        print(f"❌ 網路錯誤：{e}")
    except Exception as e:
        print(f"❌ 未知錯誤：{e}")


if __name__ == "__main__":
    while True:
        check_ticket()
        time.sleep(5)  # 每 5 秒檢查一次
