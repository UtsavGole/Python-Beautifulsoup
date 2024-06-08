import requests
from bs4 import BeautifulSoup

with open('C:/Learning/Python-Beautifulsoup/basichtml tag/sample.html','r') as f:
    content=f.read()
   # print(content)

    soup=BeautifulSoup(content,'lxml')
    #print(soup.prettify())

    #to search all the h5 tag inside the content
    cources_html_tags =soup.find_all('h5')

    #to extract title from course tag
    # for course in cources_html_tags:
    #     print(course.text)

    
    course_card=soup.find_all('div',class_='card')
    for course in course_card:
        course_name=course.h5.text
        course_price=course.a.text.split()[-1]
        print(f'the price of {course_name} is {course_price} ')
        
    
    

