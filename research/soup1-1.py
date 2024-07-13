
# https://howkteam.vn/d/thu-vien-beautiful-soup-460

from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0L1x0DM4mpSt97%2ftYgbxlC2B7n4pvJNhhvRwo8bxiO4B" class="sister" id="link1">Elsie</a>,
<a href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0OPun6GIXb9bh0UOloN9WCYbJtHZQd%2fvB08D2UeudkPP" class="sister" id="link2">Lacie</a> and
<a href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0LirHL60gbBHH3VIishi9CqgtHAKmbGoKNvFheNkumnh" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>"""

soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.title)
# <title>The Dormouse's story</title>

print(soup.title.name)
# title

print(soup.title.string)
# The Dormouse's story

print('find parent:')
print(soup.title.parent.name)
# head

print('find first one by tag:')
print(soup.p)
# <p class="title"><b>The Dormouse's story</b></p>

print('find attr value of a tag:')
print(soup.p['class'])
# title

print('find first one by tag:')
print(soup.a)
# <a class="sister" href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0L1x0DM4mpSt97%2ftYgbxlC2B7n4pvJNhhvRwo8bxiO4B" id="link1">Elsie</a>

print('find all by tag:')
print(soup.find_all('a'))
# [<a class="sister" href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0L1x0DM4mpSt97%2ftYgbxlC2B7n4pvJNhhvRwo8bxiO4B" id="link1">Elsie</a>,
# <a class="sister" href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0OPun6GIXb9bh0UOloN9WCYbJtHZQd%2fvB08D2UeudkPP" id="link2">Lacie</a>,
# <a class="sister" href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0LirHL60gbBHH3VIishi9CqgtHAKmbGoKNvFheNkumnh" id="link3">Tillie</a>]

print('find by id:')
print(soup.find(id="link3"))
# <a class="sister" href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0LirHL60gbBHH3VIishi9CqgtHAKmbGoKNvFheNkumnh" id="link3">Tillie</a>

print('find all by tag:')
for link in soup.find_all('a'):
    print(link.get('href'))
# http://example.com/elsie
# http://example.com/lacie
# http://example.com/tillie

print('find all text:')
print(soup.get_text())
# The Dormouse's story
#
# The Dormouse's story
#
# Once upon a time there were three little sisters; and their names were
# Elsie,
# Lacie and
# Tillie;
# and they lived at the bottom of a well.
#
# ...