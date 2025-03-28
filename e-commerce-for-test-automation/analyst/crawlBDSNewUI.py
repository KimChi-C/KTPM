from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import mysql.connector
from mysql.connector import Error
import datetime
from webdriver_manager.chrome import ChromeDriverManager

# URL nguồn dữ liệu
URL_CRAWL = "https://batdongsan.com.vn/nha-dat-ban-buon-ma-thuot-ddl"

# Cấu hình Chrome Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(6)  # Đợi tối đa 6 giây để tìm thấy phần tử trên trang

# Kết nối MySQL
try:
    print('🟢 Kết nối MySQL...')
    connection = mysql.connector.connect(
        host='localhost',
        database='bds_crawl',
        user='root',
        password='Y649394$'
    )
    cursor = connection.cursor()

    # Tạo bảng nếu chưa có
    create_table_query = """
    CREATE TABLE IF NOT EXISTS BATDONGSAN (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        image VARCHAR(255),
        uptime VARCHAR(50),
        price VARCHAR(50),
        distcity VARCHAR(100),
        space VARCHAR(50)
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("✅ Bảng BATDONGSAN đã sẵn sàng!")

except Error as e:
    print(f"❌ Lỗi kết nối MySQL: {e}")
    exit()  # Thoát nếu không kết nối được MySQL

# Lặp qua các trang để lấy dữ liệu
COUNT = 1
MAX_PAGE = 10  # Chỉ crawl 10 trang đầu tiên

while COUNT <= MAX_PAGE:
    print(f"🔎 Đang crawl trang {COUNT}...")
    driver.get(URL_CRAWL + f"/p{COUNT}")

    # Tìm các tin đăng trên trang
    listItem = driver.find_elements(By.CSS_SELECTOR, '.js__product-link-for-product-id')

    for item in listItem:
        try:
            title = item.find_element(By.CSS_SELECTOR, '.js__card-title').text
            price = item.find_element(By.CSS_SELECTOR, '.re__card-config-price').text
            distCity = item.find_element(By.CSS_SELECTOR, '.re__card-location').text
            productArea = item.find_element(By.CSS_SELECTOR, '.re__card-config-area').text
            uptime = datetime.date.today().strftime("%Y-%m-%d")

            print(f"🏠 {title} | 💰 {price} | 📍 {distCity} | 📏 {productArea}")

            # Chèn dữ liệu vào MySQL
            insert_query = """
            INSERT INTO BATDONGSAN (title, description, image, uptime, price, distcity, space) 
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (title, "", "", uptime, price, distCity, productArea))
            connection.commit()

        except NoSuchElementException:
            print("⚠️ Lỗi: Không thể lấy dữ liệu của một mục!")

    COUNT += 1  # Chuyển sang trang tiếp theo

# Đóng kết nối và trình duyệt
cursor.close()
connection.close()
driver.quit()
print("✅ Crawl hoàn tất! Dữ liệu đã được lưu vào MySQL.")
