import pyautogui
import time

print("Di chuyển chuột đến vị trí bạn muốn lấy tọa độ trong 5 giây...")
time.sleep(5)  # Đợi 5 giây để bạn có thời gian di chuyển chuột

# Lấy tọa độ hiện tại của con trỏ
x, y = pyautogui.position()
print(f"Tọa độ x: {x}, Tọa độ y: {y}")