import sys
# Thư viện Selenium Automation Testing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# Thư viện HTML Parser
from bs4 import BeautifulSoup
# Lưu trữ và xử lý data dạng bảng
import pandas as pd
# Xử lý liên quan thời gian
import time

from fb_scraping import init_webdriver
from fb_scraping import login_facebook
from fb_scraping import access_group
from fb_scraping import scrape_posts_and_comments
from fb_scraping import scrape_members

base_url = 'https://mbasic.facebook.com/'
int_max_size = sys.maxsize
post_max_page_index = 1
comment_max_page_index = 1
member_max_page_index = 1

start_time = time.time()

driver = init_webdriver()

# Lấy thông tin danh sách nhóm facebook
with open('fb_group_list.txt') as file:
    GROUP_LIST = file.readline().split('"')[1].split(',')[:-1]

# Lấy thông tin đăng nhập
with open('fb_credentials.txt') as file:
    EMAIL = file.readline().split('"')[1]
    PASSWORD = file.readline().split('"')[1]

# Mở trang Facebook và đăng nhập
login_facebook(driver, EMAIL, PASSWORD)

append_header = True
for group in GROUP_LIST:    
    
    print('craping "' + group + '" started')    
    group_start_time = time.time()

    # Truy cập 1 nhóm cụ thể    
    group_based_url = 'https://mbasic.facebook.com/groups/' + group + '/'
    print('group access started: ' + group_based_url)
    group_id = access_group(driver, group_based_url)
    print('->group access completed')

    # Lấy group id của 1 nhóm cụ thể
    print(' group id: ' + group_id)
    
    # Thu thập dữ liệu
    print('posts and comments scraping started')
    posts, comments = scrape_posts_and_comments(driver, group, post_max_page_index, comment_max_page_index)
    print('->posts and comments scraping completed')

    # print('members scraping started')
    # admin_members = scrape_members(driver, group_id, 'admin_moderator', member_max_page_index)
    # other_members = scrape_members(driver, group_id, 'nonfriend_nonadmin', member_max_page_index)
    # print('->members scraping completed')

    # Đóng trình duyệt
    #driver.quit()
    print('=>scraping "' + group + '" completed')
    
    print('save data "' + group + '" started')
    # Lưu dữ liệu members vào file CSV
    # members = admin_members
    # members.extend(other_members)
    # members_df = pd.DataFrame(members)
    # members_df.to_csv('members.csv', mode='a', index=False, header=False)

    # Lưu dữ liệu posts và comments vào file CSV
    posts_df = pd.DataFrame(posts)
    comments_df = pd.DataFrame(comments)
    posts_df.to_csv('posts.csv', mode='a', index=False, header=append_header)
    comments_df.to_csv('comments.csv', mode='a', index=False, header=append_header)
    print('->save data "' + group + '" completed')
    
    append_header = False
    
    group_end_time = time.time()
    print(f'Group execution time: {round(group_end_time - group_start_time)} seconds')    

end_time = time.time()
print(f'Execution time: {round(end_time - start_time)} seconds')




