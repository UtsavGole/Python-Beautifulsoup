from bs4 import BeautifulSoup
import requests
import json


def find_jobs():
    filter=input('Enter skills you want to filter: ')
    print(f'Fltering : {filter}')
    url='https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation='
    html_text=requests.get(url).text

    soup=BeautifulSoup(html_text,'lxml')

    jobs=soup.find_all('li',class_='clearfix job-bx wht-shd-bx')


    record=[]

    for job in jobs:

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

            job_detail={
                "job_name":job_name,
                "company_name":company_name,
                "key_skill":key_skill,
                "more_info":more_info,
                "published_date":published_date
            }
            if filter in key_skill:
                record.append(job_detail)

    return record

def write_to_json(records):
    with open(f'data/job_records.json','w') as f:
        json.dump(records,f,indent=2)


                 #print(f'File Saved:{index}')
              
if __name__=="__main__":              
    records=find_jobs()
    write_to_json(records)

