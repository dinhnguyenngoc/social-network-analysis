from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Cấu hình Selenium
options = Options()
options.add_argument("--disable-notifications")
service = Service('/usr/local/bin/chromedriver')  # Đường dẫn đến chromedriver trên máy của bạn
driver = webdriver.Chrome(service=service, options=options)

# Đăng nhập vào Facebook
def login_facebook(email, password):
    driver.get('https://www.facebook.com/')
    time.sleep(3)
    
    email_input = driver.find_element(By.ID, 'email')
    password_input = driver.find_element(By.ID, 'pass')
    
    email_input.send_keys(email)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

# Truy cập vào nhóm cụ thể
def access_group(group_url):
    driver.get(group_url)
    time.sleep(5)

# Cuộn trang để tải thêm nội dung
def scroll_page():
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    page_index = 1
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        page_index += 1
        if page_index > 2:
            break

# Thu thập dữ liệu bài viết và bình luận
def scrape_posts_and_comments():
    post_data = []
    comment_data = []

    scroll_page()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    posts = soup.find_all('div', {'role': 'article'})

    for post in posts:
        post_id = post.get('id')
        author_tag = post.find('a', {'role': 'link'})
        author_id = author_tag.get('href').split('?')[0] if author_tag else 'N/A'
        post_data.append({'postid': post_id, 'authorid': author_id})

        comments = post.find_all('div', {'aria-label': 'Comment'})
        for comment in comments:
            comment_id = comment.get('id')
            comment_author_tag = comment.find('a', {'role': 'link'})
            comment_author_id = comment_author_tag.get('href').split('?')[0] if comment_author_tag else 'N/A'
            comment_data.append({'commentid': comment_id, 'authorid': comment_author_id})

    return post_data, comment_data

# Thu thập dữ liệu thành viên
def scrape_members():
    member_data = []

    driver.get(driver.current_url + '/members/near_you')
    time.sleep(5)
    
    scroll_page()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    members = soup.find_all('div', {'role': 'listitem'})

    for member in members:
        member_tag = member.find('a', {'role': 'link', 'tabindex': '-1'})
        member_id = member_tag.get('href').split('/user/')[1][:-1] if member_tag else 'N/A'
        member_name = member_tag.get('aria-label') if member_tag else 'N/A'
        
        #member_contribution_tag = member.find('a', {'role': 'link', 'tabindex': '0'})
        #member_contribution_point = member_contribution_tag.text
        
        member_type_tag = member.find('span', {'class': 'member_type'})
        member_type = member_type_tag.text if member_type_tag else 'N/A'
        member_data.append({'member_id': member_id, 'member_name': member_name, 'member_type': member_type})

    return member_data

# Đăng nhập
login_facebook('your_email', 'your_pass')

# Truy cập nhóm
access_group('https://www.facebook.com/groups/your_group')

# Thu thập dữ liệu
#posts, comments = scrape_posts_and_comments()
members = scrape_members()

# Đóng trình duyệt
driver.quit()

# In kết quả (có thể lưu vào file hoặc cơ sở dữ liệu tùy nhu cầu)
#print("Posts:", posts)
#print("Comments:", comments)
print("Members:", members)

# Lưu dữ liệu vào file CSV
members_df = pd.DataFrame(members)

members_df.to_csv('members.csv', index=False)
