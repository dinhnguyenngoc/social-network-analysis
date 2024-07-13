
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

print(soup.prettify())


# <html>
#  <head>
#   <title>
# The Dormouse's story
#   </title>
#  </head>
#  <body>
#   <p class="title">
# <b>
#     The Dormouse's story
# </b>
#   </p>
#   <p class="story">
# Once upon a time there were three little sisters; and their names #     were
# <a class="sister" href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0L1x0DM4mpSt97%2ftYgbxlC2B7n4pvJNhhvRwo8bxiO4B" id="link1">
# Elsie
# </a>
# ,
# <a class="sister" href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0OPun6GIXb9bh0UOloN9WCYbJtHZQd%2fvB08D2UeudkPP" id="link2">
# Lacie
# </a>
# and
# <a class="sister" href="/redirect?Id=f%2fKgPq4IDV0SyEq0zfYr0LirHL60gbBHH3VIishi9CqgtHAKmbGoKNvFheNkumnh" id="link2">
# Tillie
# </a>
# ; and they lived at the bottom of a well.
#   </p>
#   <p class="story">
# ...
#   </p>
#  </body>
# </html>
