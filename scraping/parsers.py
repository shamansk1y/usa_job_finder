import codecs
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import requests
import os

# __all__ = ('indeed', 'linkedin', 'zip_recruiter', 'dice', 'ladders', 'flexjobs' , 'builtin', 'themuse')
__all__ = ('indeed', 'linkedin', 'dice', 'flexjobs' , 'builtin', 'themuse')
ua = UserAgent()
headers = {'User-Agent': ua.random}

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')

def initialize_driver(url):
    # local config
    # service = Service()
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(service=service, options=chrome_options)


    # deploy config
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    
    driver.get(url)

    time.sleep(10)
    return driver

def close_driver(driver):
    driver.quit()


def indeed(url, city=None, language=None):
    driver = initialize_driver(url)
    html = driver.page_source

    domain = 'https://www.indeed.com'
    jobs = []
    errors = []

    try:
        if html:
            soup = BS(html, 'html.parser')
            main_div = soup.find('div', 'mosaic-provider-jobcards')
            li_list = main_div.find_all('li', 'eu4oa1w0')

            for item in li_list:
                title = item.find('h2')
                if title:
                    title_link = title.find('a')
                    if title_link:
                        href = title_link['href']
                        content = item.ul.text

                        company_el = item.find('span', 'companyName')
                        if company_el:
                            company = company_el.text

                        jobs.append({'title': title.text if title else None,
                                     'url': domain + href if href else None,
                                     'description': content if content else None,
                                     'company': company if company else None})
        else:
            errors.append({'url': url, 'title': "HTML is empty"})
    except Exception as e:
        errors.append({'url': url, 'title': str(e)})

    close_driver(driver)
    return jobs, errors

def linkedin(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', 'base-serp-page__content')
            job_lst = main_div.find_all('li')
            if job_lst:
                for job in job_lst:
                    title = job.find('h3', 'base-search-card__title').get_text(strip=True)
                    a_element = job.find('div', class_='base-card').find('a', class_='base-card__full-link')

                    href = a_element.get('href')
                    content = ''
                    company = job.find('h4', 'base-search-card__subtitle').get_text(strip=True)

                    jobs.append({'title': title, 'url': href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


# def zip_recruiter(url, city=None, language=None):
#     driver = initialize_driver(url)
#     html = driver.page_source

#     jobs = []
#     errors = []

#     if html:
#         soup = BS(html, 'html.parser')
#         job_articles = soup.find_all('article', class_='new_job_item')

#         for article in job_articles:
#             job_title = article.find('h2', class_='title').get_text(strip=True)
#             company_name = article.find('span', class_='company_name').get_text(strip=True)
#             href_div = article.find('div', 'job_title_raw')
#             href = href_div.a['href']
#             content = article.find('p', 'job_snippet').get_text(strip=True)

#             jobs.append({'title': job_title, 'url': href,
#                          'description': content, 'company': company_name,
#                          'city_id': city, 'language_id': language})
#     else:
#         errors.append({'url': url, 'title': "Div does not exists"})

#     close_driver(driver)
#     return jobs, errors



def dice(url, city=None, language=None):
    driver = initialize_driver(url)
    html = driver.page_source

    jobs = []
    errors = []

    if html:
        soup = BS(html, 'html.parser')
        job_cards = soup.find_all('div', 'card search-card')
        for job in job_cards:
            job_title = job.find('h5')
            title =job_title.a.text.strip()
            href = job_title.a['href']
            company_el = job.find('div', 'card-company')
            company = company_el.a.text.strip()
            content = job.find('div', {'data-cy': 'card-summary'}).get_text(strip=True)
            jobs.append({'title': title, 'url': href,
                         'description': content, 'company': company,
                         'city_id': city, 'language_id': language})
    else:
        errors.append({'url': url, 'title': "Page do not response"})
    close_driver(driver)
    return jobs, errors


# def ladders(url, city=None, language=None):
#     driver = initialize_driver(url)
#     html = driver.page_source
#     domain = 'https://www.theladders.com'
#     jobs = []
#     errors = []

#     if html:
#         soup = BS(html, 'html.parser')
#         main_div = soup.find('div', 'job-list-pagination-jobs')

#         if main_div:  # Проверка, что main_div был найден
#             job_cards = main_div.find_all('div', 'guest-job-card-container')
#             if job_cards:
#                 for job in job_cards:
#                     job_title = job.find('div', 'job-card-text-container')
#                     title_el = job_title.find('p', 'job-link-wrapper')
#                     title = title_el.a.text.strip()
#                     href = title_el.a['href']
#                     company = job.find('span', 'job-card-company-name').get_text(strip=True)
#                     content = job.find('p', 'job-card-description').get_text(strip=True)

#                     jobs.append({'title': title, 'url': domain + href,
#                                  'description': content, 'company': company,
#                                  'city_id': city, 'language_id': language})
#             else:
#                 errors.append({'url': url, 'title': "No job cards found"})
#         else:
#             errors.append({'url': url, 'title': "No main_div found"})
#     else:
#         errors.append({'url': url, 'title': "Page do not response"})

#     close_driver(driver)
#     return jobs, errors


def is_valid_job(title):
    keywords = ['python', 'django', 'flask']
    return   any(keyword in title.lower() for keyword in keywords)


def flexjobs(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.flexjobs.com'
    if url:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            job_lst = soup.find_all('li', 'm-0 row job clickable')
            if job_lst:
                for job in job_lst:
                    title = job.get('data-title')
                    if is_valid_job(title):
                        href_el = job.find('a', 'job-title job-link')
                        href = href_el['href']
                        company = ''
                        content_el = job.find('div', 'job-description')
                        content = content_el.get_text(strip=True) if content_el else ''
                        jobs.append({'title': title, 'url': domain + href,
                                     'description': content, 'company': company,
                                     'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors



def builtin(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://builtin.com'
    if url:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', 'd-flex gap-sm flex-column')
            job_lst = main_div.find_all('div', attrs={'data-id':'job-card'})
            if job_lst:
                for job in job_lst:
                    title = job.find('h2').get_text(strip=True)
                    href_el = job.find('h2').find('a')
                    href = href_el.get('href') if href_el else ''
                    content = ''
                    company_el = job.find('div', attrs={'data-id':'company-title'})
                    company = company_el.find('span').get_text(strip=True)

                    jobs.append({'title': title, 'url': domain + href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors


def themuse(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.themuse.com/'
    if url:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            job_lst = soup.find_all('div', 'JobCard_jobCardClickable__ZR6Sk JobCard_jobCard__jQyRD')
            if job_lst:
                for job in job_lst:
                    title = job.find('h2').get_text(strip=True)

                    href_el = job.find('a', 'JobCard_viewJobLink__Gesny')
                    href = href_el.get('href') if href_el else ''
                    content = ''
                    company_el = job.find('div', 'JobCard_companyLocation__KBfg2')
                    company = company_el.find('a').get_text(strip=True)

                    jobs.append({'title': title, 'url': domain + href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors




if __name__ == '__main__':
    url = 'https://www.ziprecruiter.com/Jobs/Entry-Level-Python-Developer'
    jobs, errors = zip_recruiter(url)
    h = codecs.open('zip_recruiter.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
