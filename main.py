from bs4 import BeautifulSoup
import requests
import os
#from requests_html import HTMLSession
import json

url='https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords=python&postWeek=60&searchType=personalizedSearch&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&pDate=I&sequence=1&startPage=1'
html_text=requests.get(url).text
soup=BeautifulSoup(html_text,'lxml')

#searching em tags
em_tags=soup.find_all('em')

#spliting page URL
def find_base_url(url):
    base_url=url.split('&startPage=1')
    og_url=base_url[0][:-1]
    return og_url

jobs_url_base=find_base_url(url)
print(jobs_url_base)

#extracting page number of websites
def page_number(em_tags):
    page_number=[]
    for em in em_tags:
        if em.get('class') and 'active' in em['class']:
            page_number.append(em.get_text())
        elif em.a:

            page_number.append(em.a.get_text())
    return(len(page_number))

pg_num=page_number(em_tags)

#extracting list of web pages
def jobs_url(url,page_num):
    print(page_num)
    print(url)
    jobs_url_list=[]
    for page in range(1,page_num):
        job_page_url=url+str(page)+'&startPage=1'
        jobs_url_list.append(job_page_url)
    return(jobs_url_list)

pages_url_list=jobs_url(jobs_url_base,pg_num)
#print(pages_url_list)

#Function to save the last scrapped page
def save_last_scrapped_url(last_scraped_url,last_url_file='last_url.txt'):
    with open(last_url_file,'w') as file:
        file.write(last_scraped_url)

#Function to load the lst scrapped URL
def load_last_scraped_url(last_url_file='last_url.txt'):
    if os.path.exists(last_url_file):
        with open(last_url_file,'r') as file:
            return file.read().strip()
    return None


#extracting deatil of jobs from each page
def extract_records(job_url_list):

    last_scraped_url=load_last_scraped_url()

    if last_scraped_url:
        try:
            last_scraped_index=job_url_list.index(last_scraped_url)
            job_url_list=job_url_list[last_scraped_index+1:]

        except ValueError:
            pass


    record=[]
    for jobs in job_url_list:
        job_html_text=requests.get(jobs).text
        soups=BeautifulSoup(job_html_text,'lxml')
        jobss=soups.find_all('li',class_='clearfix job-bx wht-shd-bx')
        print(jobs)

        for job in jobss:
            published_date=job.find('span',class_='sim-posted').span.text.strip()
        #print(published_date)

            #if 'few' in published_date.lower():

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
                "experience year":exp_year,
                "published_date":published_date
            }
            #if filter in key_skill:
            record.append(job_detail)
        save_last_scrapped_url(jobs)

    return record




#dumping extracted data into json
def write_to_json(records):
    with open(f'data/job_records_multiple_pagesss.json','w') as f:
        json.dump(records,f,indent=2)


                 #print(f'File Saved:{index}')
            
if __name__=="__main__":              
    records=extract_records(pages_url_list)
    write_to_json(records)

