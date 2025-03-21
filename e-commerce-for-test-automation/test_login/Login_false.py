from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo trình duyệt
driver = webdriver.Chrome()  
driver.maximize_window()

# Mở trang login
driver.get("https://www.saucedemo.com/")

# Nhập Username và Password SAI
driver.find_element(By.ID, "user-name").send_keys("wrong_user")
driver.find_element(By.ID, "password").send_keys("wrong_password")

# Click Login
driver.find_element(By.ID, "login-button").click()

# Chờ load lỗi
time.sleep(3)

# Kiểm tra lỗi hiển thị
error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
if "Epic sadface: Username and password do not match" in error_message:
    print("✅ Test thất bại đúng như mong đợi!")
else:
    print("❌ Test không đúng, không thấy thông báo lỗi!")

# Đóng trình duyệt
driver.quit()
