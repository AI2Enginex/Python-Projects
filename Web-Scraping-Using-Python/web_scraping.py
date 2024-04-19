import os
import time
import requests
from csv import writer
from bs4 import BeautifulSoup

class WebScraping:
    
    def __init__(self, job_role=None,url=None):
        # Constructor to initialize the WebScraping object
        self.unfamilier_skill = input('>')  # Get unfamiliar skill from user input
        self.job_role = job_role  # Set job role
        self.url = url # url for scraping data
    
    def find_jobs(self):
        # Function to find job listings from the website
        html_page = requests.get(self.url)
        soup = BeautifulSoup(html_page.text, 'lxml')
        self.jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')  # Extract job listings
    
    def write(self):
        # Function to write job listings to CSV file
        self.find_jobs()  # Get job listings
        if not os.path.isfile('jobs.csv'):  # If CSV file doesn't exist, create it
            with open('jobs.csv', 'w', encoding='utf-8', newline='') as f:
                thewriter = writer(f)
                # Write header to CSV file
                header = ['company_name', 'skills_required', 'not required', 'job role', 'more_info']
                thewriter.writerow(header)
                # Function to write job information to CSV file
                def write_file():
                    for job in self.jobs:
                        job_posted = job.find('span', class_='sim-posted').text
                        if 'few' in job_posted:
                            company_name = job.find('h3', class_='joblist-comp-name').text.replace('\n', '').replace('\r', '')
                            skills_required = job.find('span', class_='srp-skills').text.replace('\n', '').replace('\r', '').lower()
                            not_required = self.unfamilier_skill
                            job_role = self.job_role
                            more_info = job.header.h2.a['href']
                            if self.unfamilier_skill not in skills_required:
                                info = [company_name, skills_required, not_required, job_role, more_info]
                                thewriter.writerow(info)  # Write job information to CSV file
                                print('')
                write_file()  # Call function to write job information
        else:
            with open('jobs.csv', 'a', encoding='utf-8', newline='') as f:
                thewriter = writer(f)
                # Function to write job information to CSV file
                def write_file():
                    for job in self.jobs:
                        job_posted = job.find('span', class_='sim-posted').text
                        if 'few' in job_posted:
                            company_name = job.find('h3', class_='joblist-comp-name').text.replace('\n', '').replace('\r', '')
                            skills_required = job.find('span', class_='srp-skills').text.replace('\n', '').replace('\r', '').lower()
                            not_required = self.unfamilier_skill
                            job_role = self.job_role
                            more_info = job.header.h2.a['href']
                            if self.unfamilier_skill not in skills_required:
                                info = [company_name, skills_required, not_required, job_role, more_info]
                                thewriter.writerow(info)  # Write job information to CSV file
                                print('')
                write_file()  # Call function to write job information

if __name__ == '__main__':
    while True:
        # Main program
        w = WebScraping(job_role='python',url='https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=')  # Create WebScraping object
        w.write()  # Write job listings to CSV file
        time_wait = 10  # Set time interval for scraping
        print(f'waiting for {time_wait} seconds...')
        time.sleep(time_wait)  # Wait for specified time interval
