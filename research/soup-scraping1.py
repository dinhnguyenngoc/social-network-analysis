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

# Cấu hình Selenium
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
#options.add_argument("--headless")  # Chạy Chrome ở chế độ headless (không hiển thị giao diện)
service = Service('/usr/local/bin/chromedriver')  # Đường dẫn đến chromedriver trên máy
driver = webdriver.Chrome(service=service, options=options)
base_url = 'https://mbasic.facebook.com/'
group_id = 'N/A'

# Đăng nhập vào Facebook
def login_facebook(email, password):
    print('open facebook started')
    driver.get(base_url)
    time.sleep(3)
    print('->open facebook completed')
    
    print('login started')
    email_input = driver.find_element(By.NAME, 'email')
    password_input = driver.find_element(By.NAME, 'pass')
    
    email_input.send_keys(email)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)
    print('->login completed')

# Truy cập vào nhóm cụ thể
def access_group(group_url):
    driver.get(group_url)
    time.sleep(3)    

# Truy cập vào link cụ thể
def access_link(link_url):
    driver.get(link_url)
    time.sleep(3)

# Lấy group id của 1 nhóm cụ thể
def get_group_id():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    about_tag = soup.find('a', string="About")
    return about_tag.get('href').split('?')[0][8:]

# Cuộn trang để tải thêm nội dung
def scroll_page():        
    
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    #page_index = 1
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        #page_index += 1
        #if page_index > 6:
        #    break

def get_more_posts():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
            
    more_posts_tag = soup.find('a', string="See more posts")
    if more_posts_tag is not None:
        link = base_url + more_posts_tag.get('href')[1:]
        access_link(link)
        return True
    return False
    
    # Tìm thẻ <a>See more posts</a> và click vào
    # try:            
    #     link = driver.find_element(By.LINK_TEXT, "See more posts")
    #     link.click()
    # except Exception as e:
    #     print("Không thể tìm thấy thẻ <a>See more posts</a> hoặc click vào nó:", e)

    # Đợi một lúc để kiểm tra kết quả
    # time.sleep(3)

def get_more_comments(post_id):
    soup2 = BeautifulSoup(driver.page_source, 'html.parser')

    see_next_id = "see_next_" + post_id
    more_comments_tag = soup2.find('div', id=see_next_id)
    more_comments_tag = more_comments_tag.find('a')
    if more_comments_tag is not None:        
        link = base_url + more_comments_tag.get('href')[1:]
        access_link(link)
        return True
    return False

def get_more_members():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
            
    more_members_tag = soup.find('a', string="See more")
    if more_members_tag is not None:        
        link = base_url + more_members_tag.get('href')[1:]
        access_link(link)
        return True
    return False

# Thu thập dữ liệu bài viết và bình luận
def scrape_posts_and_comments():
    post_data = []
    comment_data = []

    post_page_index = 1
    while True:
        print(' post page: ' + str(post_page_index))
            
        scroll_page()
    
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Tìm thẻ cha chứa các bài viết
        feed = soup.find('div', {'id': 'm_group_stories_container'})
        # Tìm tất cả các bài viết
        posts = feed.find('section').find_all('article',recursive=False)

        # Duyệt qua từng bài viết
        for post in posts:
            is_shared = False            
            # isShared: true if the post contains an original object shared on the group, false otherwise
            if post.find('article') is not None:
                is_shared = True
            
            # Post header
            post_header_tag = post.find('header')
            author_name = 'N/A'
            author_id = 'N/A'        
            if post_header_tag is not None:
                # Lấy tên người đăng        
                if post_header_tag.find('a') is not None:
                    author_name = post_header_tag.find('a').text
                    # authorId: identifier of the author
                    if post_header_tag.find('a').get('href') is not None:
                        author_id = post_header_tag.find('a').get('href').split('?')
                        if author_id[0] != '/profile.php':
                            author_id = author_id[0][1:]
                        else:
                            author_id = author_id[1].split('&')[0][3:]
                                                
            # Post data
            post_data_tag = post_header_tag.next_sibling
            if is_shared:
                post_data_tag = post.find('article')
            post_content = 'N/A'        
            if post_data_tag is not None:
                # Lấy nội dung bài viết        
                if post_data_tag.find('p') is not None:
                    post_content = post_data_tag.find('p').text
                if post_data_tag.find('span') is not None:
                    post_content = post_data_tag.find('span').text
                
                post_content = post_data_tag.get_text()

            # Post footer
            post_footer_tag = post.find('footer')
            time_creation = 'N/A'
            reactions = 'N/A'
            post_id = 'N/A'
            if post_footer_tag is not None:
                # timeCreation: creation time   
                if post_footer_tag.find('abbr') is not None:
                    time_creation = post_footer_tag.find('abbr').text
                # reactions: the number of reactions (Like, Love, Haha, Wow, Sad, Angry)          
                if post_footer_tag.find('a') is not None:
                    reactions = post_footer_tag.find('a').text
                # postId: identifier of the post
                if post_footer_tag.find('a', string="Full Story") is not None:
                    post_id = post_footer_tag.find('a', string="Full Story").get('href').split('/')[6]                
            
            print('  ', post_id, author_id, author_name)
            
            # Thêm dữ liệu bài viết vào danh sách post_data
            post_data.append({'postId': post_id, 'author_id': author_id, 'authorName': author_name, 'time': time_creation, 'isShared': is_shared, 'postContent': post_content, 'reactions': reactions})

            # Lấy tất cả bình luận từ 1 bài viết cụ thể
            post_id = '3827105437612569'
            comment_data = scrape_comments(post_id)

        post_page_index += 1
        if post_page_index > 1:
            break
        is_more_posts = get_more_posts()
        if is_more_posts == False:
            break
            
    return post_data, comment_data

def scrape_comments(post_id):
    comment_data = []
    
    # Truy cập vào trang comments của 1 bài viết cụ thể
    driver.get(group_based_url + 'permalink/' + post_id)
    time.sleep(3)
    
    comment_page_index = 1
    while True:
        print('     comment page: ' + str(comment_page_index))
            
        scroll_page()
    
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
                    
        # Tìm thẻ cha chứa tất cả các bình luận            
        comments = soup2.find('div', {'id': 'add_comment_switcher_placeholder'})
        comments = comments.next_sibling.next_sibling.next_sibling
        comments = comments.children
                        
        # Duyệt qua từng bình luận
        for comment in comments:
            comment_id = 'N/A'
            comment_author_id = 'N/A'
            comment_author_name = 'N/A'
            comment_content = 'N/A'
            comment_reactions = 'N/A'
            comment_id = comment.get('id')
            # Kiểm tra nếu bài viết không có comment
            if comment_id is None:
                continue     
            # Kiểm tra nếu không còn comment nào khác
            if comment_id == ('see_next_' + str(post_id)):
                continue
            
            comment_tag = comment.find('a')
            if comment_tag is not None:
                comment_author_name = comment_tag.text
                if comment_tag.parent is not None:
                    if comment_tag.parent.next_sibling is not None:
                        comment_content = comment_tag.parent.next_sibling.text
                #comment_author_id = comment_tag.get('href').split('?')[0][1:]                
                comment_author_id = comment_tag.get('href').split('?')
                if comment_author_id[0] != '/profile.php':
                    comment_author_id = comment_author_id[0][1:]
                else:
                    comment_author_id = comment_author_id[1].split('&')[0][3:]
            reactions_tag = comment.find('a', string="Like")
            if reactions_tag is not None:                    
                try:
                    reactions_tag = reactions_tag.previous_sibling.previous_sibling
                    comment_reactions = reactions_tag.text
                except Exception as e:
                    comment_reactions = 0
                                                                            
            print('      ' + post_id, comment_id, comment_author_id)
                                                                
            # Thêm dữ liệu bình luận vào danh sách comment_data
            comment_data.append({'postId': post_id, 'commentId': comment_id, 'authorId': comment_author_id, 'authorName': comment_author_name, 'commentContent': comment_content, 'reactions': comment_reactions})                                        

        comment_page_index += 1
        if comment_page_index > 5:
            break
        is_more_comments = get_more_comments(post_id)
        if is_more_comments == False:
            break
        
    return comment_data

# Thu thập dữ liệu thành viên
def scrape_members(member_type):
    member_data = []

    driver.get(base_url + 'browse/group/members/?id=' + group_id + '&start=0&listType=list_' + member_type)
    time.sleep(3)
    
    print(' ' + member_type)
    member_page_index = 1
    while True:
        print(' page: ' + str(member_page_index))                    
    
        scroll_page()
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Tìm thẻ cha chứa các thành viên và tìm tất cả các thành viên
        members = soup.find(id='objects_container').find_all('table')

        for member in members:
            member_tag = member.find('a')
            member_id = 'N/A'
            member_name = 'N/A'
            if member_tag is not None:
                # memberId: the identifier of a member                
                member_id = member_tag.get('href').split('?')
                if member_id[0] != '/profile.php':
                    member_id = member_id[0][1:]
                else:
                    member_id = member_id[1].split('&')[0][3:]
                # memberName: the name of a member
                member_name = member_tag.text
            
            print('  ', member_id, member_name)
            
            # memberType: the type of the members (0 = admins & moderators, 1 = members with things in common, 2 = members who contribute to the group, 3 = member recently joined
            member_data.append({'memberId': member_id, 'memberName': member_name, 'memberType': member_type})

        member_page_index += 1
        if member_page_index > 2:
            break
        is_more_members = get_more_members()
        if is_more_members == False:
            break

    return member_data

# Lấy thông tin đăng nhập
with open('fb_credentials.txt') as file:
    EMAIL = file.readline().split('"')[1]
    PASSWORD = file.readline().split('"')[1]

# Mở trang Facebook và đăng nhập
login_facebook(EMAIL, PASSWORD)

print('craping started')

# Truy cập 1 nhóm cụ thể
group_based_url = 'https://mbasic.facebook.com/groups/VM.2019/'
print('group access started: ' + group_based_url)
access_group(group_based_url)
print('->group access completed')

# Lấy group id của 1 nhóm cụ thể
group_id = get_group_id()
print(' group id: ' + group_id)

# Thu thập dữ liệu
print('posts and comments scraping started')
posts, comments = scrape_posts_and_comments()
print('->posts and comments scraping completed')

# print('members scraping started')
# admin_members = scrape_members('admin_moderator')
# other_members = scrape_members('nonfriend_nonadmin')
# print('->members scraping completed')

# Đóng trình duyệt
driver.quit()
print('=>scraping completed')

# In kết quả (có thể lưu vào file hoặc cơ sở dữ liệu tùy nhu cầu)
#print("Posts:", posts)
#print("Comments:", comments)
#print("Members:", members)

print('save data started')
# Lưu dữ liệu members vào file CSV
# members = admin_members
# members.extend(other_members)
# members_df = pd.DataFrame(members)
# members_df.to_csv('members.csv', index=False)

# Lưu dữ liệu posts và comments vào file CSV
posts_df = pd.DataFrame(posts)
comments_df = pd.DataFrame(comments)
posts_df.to_csv('posts.csv', index=False)
comments_df.to_csv('comments.csv', index=False)
print('->save data completed')