from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Khởi tạo WebDriver cho trình duyệt Chrome
driver = webdriver.Chrome()

# Mở trang web
driver.get("http://www.google.com")

# Tìm phần tử input của Google bằng tên
search_box = driver.find_element(By.NAME, "q")

# Nhập văn bản vào ô tìm kiếm
search_box.send_keys("Selenium WebDriver")

# Nhấn phím Enter để tìm kiếm
search_box.send_keys(Keys.RETURN)

# Chờ trang tải kết quả (có thể điều chỉnh thời gian chờ phù hợp)
time.sleep(2)

# Lấy hai kết quả tìm kiếm đầu tiên
results = driver.find_elements(By.CSS_SELECTOR, 'div.g')[:2]

# In ra màn hình console
for index, result in enumerate(results, start=1):
    title = result.find_element(By.TAG_NAME, 'h3').text
    link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
    print(f"Result {index}:")
    print(f"Title: {title}")
    print(f"Link: {link}")
    print()

# Đóng trình duyệt
driver.quit()
