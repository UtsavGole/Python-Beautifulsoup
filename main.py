from bs4 import BeautifulSoup
import requests


def find_jobs():
    filterout=input('Enter skills you want to filter out: ')
    print(f'Fltering out: {filterout}')
    url='https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation='
    html_text=requests.get(url).text

    soup=BeautifulSoup(html_text,'lxml')

    jobs=soup.find_all('li',class_='clearfix job-bx wht-shd-bx')



    for index,job in enumerate(jobs):

        published_date=job.find('span',class_='sim-posted').span.text.strip()
    # print(published_date)

        if 'few' in published_date.lower():

            job_name=job.a.text.strip()
        # print(job_name)

            company_name=job.find('h3',class_='joblist-comp-name').text.strip()
        # print(company_name)

            key_skill=job.find('span',class_='srp-skills').text.replace(' ','').strip()
            #print(key_skill)

            more_info=job.header.h2.a['href']
            

            exp_year=job.find('ul',  class_='top-jd-dtl clearfix').li.text.strip('card_travel').strip()
            #print(exp_year)

            if filterout not in key_skill.lower():
                with open(f'data/{index}','w') as f:
                    f.write(f"Job Name: {job_name}  \n")
                    f.write(f"Company Name: {company_name} \n")
                    f.write(f"Required Skills: {key_skill} \n")
                    f.write(f"Exeperience Year: {exp_year} \n")
                    f.write(f"Published Date: {published_date} \n")
                    f.write(f"More info: {more_info} \n")
                print(f'File Saved:{index}')
              
find_jobs()