from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo trình duyệt
driver = webdriver.Chrome()  
driver.maximize_window()

# Mở trang login
driver.get("https://www.saucedemo.com/")

# Nhập Username và Password ĐÚNG
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")

# Click Login
driver.find_element(By.ID, "login-button").click()

# Chờ load trang
time.sleep(3)

# Kiểm tra đăng nhập thành công
if driver.current_url == "https://www.saucedemo.com/inventory.html":
    print("✅ Đăng nhập thành công!")
else:
    print("❌ Đăng nhập thất bại!")

# Đóng trình duyệt
driver.quit()
