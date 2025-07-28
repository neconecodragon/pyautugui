import subprocess
import time
import pyautogui
import pygetwindow as gw
import random
import requests

KEEP_KEYWORDS = ["watch", "chatgpt", "record"]

def get_chrome_windows():
    return [w for w in gw.getWindowsWithTitle('Chrome') if w.visible and w.title.strip() != ""]

# 1. Mở Chrome với link và kích thước cố định
old_url = "https://raw.githubusercontent.com/anisidina29/anisidina29-selenium_earnvids_docker/refs/heads/main/earnvids.txt"
response_old = requests.get(old_url)
response_old.raise_for_status()
links = response_old.text.strip().splitlines()

# 🎯 Lấy 1 link ngẫu nhiên
url = random.choice(links)
print(f"🎯 Đã chọn link: {url}")
print("🚀 Đang mở Chrome...")
subprocess.Popen(["start", "chrome", "--new-window", url, "--window-size=1280,720"], shell=True)

# 2. Chờ trình duyệt mở và tab chính load
time.sleep(6)

# 3. Tìm và click nút Play hoặc click giữa màn hình
for i in range(11):
    print(f"\n🔁 Lặp lần {i+1}/10")
    # [1] Click Play hoặc click giữa màn hình
    try:
        location = pyautogui.locateOnScreen("play.png", confidence=0.8)
        if location:
            center = pyautogui.center(location)
            pyautogui.moveTo(center.x, center.y, duration=0.3)
            pyautogui.click()
            print("✅ Đã click nút Play!")
        else:
            raise Exception("Không tìm thấy ảnh")
    except Exception as e:
        print("⚠️ Không tìm thấy play.png, đợi tab mới mở & click giữa màn hình thay thế.")


        screen_width, screen_height = pyautogui.size()

        # 🌀 Tạo vị trí x,y random quanh tâm màn hình (±50px)
        rand_x = screen_width // 2 + random.randint(-50, 50)
        rand_y = screen_height // 2 + random.randint(-50, 50)

        # Di chuyển và click
        pyautogui.moveTo(rand_x, rand_y, duration=random.uniform(0.2, 0.6))
        pyautogui.click()

    # [2] Xử lý tab: đóng tab không cần thiết
    tabs = get_chrome_windows()
    for w in tabs:
        title = w.title.lower()
        if any(k in title for k in KEEP_KEYWORDS):
            print(f"✅ Giữ tab: {w.title}")
        else:
            print(f"❌ Đóng tab: {w.title}")
            w.activate()
            time.sleep(3)
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)

    time.sleep(3)  # ⏱️ nghỉ giữa mỗi vòng lặp nếu cần

print("\n🕹️ Bắt đầu mô phỏng hoạt động người dùng trong 250 giây...")
start_time = time.time()
duration = 250  # giây

while time.time() - start_time < duration:
    # Lấy kích thước màn hình
    screen_width, screen_height = pyautogui.size()

    # Tọa độ ngẫu nhiên trong vùng màn hình
    rand_x = random.randint(100, screen_width - 100)
    rand_y = random.randint(100, screen_height - 100)

    # Di chuyển chuột ngẫu nhiên
    pyautogui.moveTo(rand_x, rand_y, duration=random.uniform(0.2, 0.5))

    # Nghỉ 2–4 giây giữa mỗi lần di chuyển
    time.sleep(random.uniform(2, 4))

print("✅ Hoàn tất mô phỏng chuột. Đang chụp màn hình...")

# 📸 Chụp màn hình
timestamp = int(time.time())
import os
os.makedirs("output", exist_ok=True)
screenshot_path = f"output/screenshot_{timestamp}.png"
pyautogui.screenshot(screenshot_path)
print(f"🖼️ Đã lưu ảnh: {screenshot_path}")
# ❌ Đóng tất cả tab Chrome còn lại
print("🧹 Đang đóng các tab Chrome còn lại...")
tabs = get_chrome_windows()
for w in tabs:
    print(f"❌ Đóng tab: {w.title}")
    w.activate()
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.5)

print("✅ Hoàn tất tất cả.")
