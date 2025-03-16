import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


job_title = []
company_name = []
location = []
date_posted = []
job_type = []
job_status = []
years_of_experience = []
level = []
skills_required = []

page = 0
base_url = "https://wuzzuf.net/search/jobs/?q=data%20analyst&a=hpb&start="
while True:
    url = base_url + str(page)
    response = requests.get(url)
    if response.status_code != 200:
        break
    soup = BeautifulSoup(response.text, "lxml")
    job_card = soup.find_all("div", class_ = "css-pkv5jc")
    for job in job_card:
            job_title.append(job.h2.text)
            company_name.append(job.find("div", class_ = "css-d7j1kk").a.text.replace(" -", "").strip())
            location.append(job.find("span", class_ ="css-5wys0k").text.strip())
            date_posted.append(job.find("div", class_ ="css-laomuu").find_next("span").find_next("div").text)
            job_type.append(job.find("span", class_ ="css-1ve4b75 eoyjyou0").text.strip())
            job_status.append(job.find("div", class_ ="css-1lh32fc").find_next("a").find_next("a").text.strip())
            level.append(job.find("div", class_ ="css-y4udm8").find_next("div").find_next("div").find("a").text.strip())
            years_of_experience.append(job.find("div", class_ ="css-y4udm8").find_next("div").find_next("span").find_next("div").find_next("span").text.replace("·", "").replace("Yrs of Exp",""))
            skills_required.append(job.find("div", class_ ="css-y4udm8").find_next("div").find_next("span").find_next("div").text) #Needs Cleaning
    print(f"{len(job_title)} jobs have been added :D")
    if not job_card:
        break
    page +=1
print("SCRAPPING IS DONE!")

df = pd.DataFrame({
     "job_title": job_title,
     "company_name": company_name,
    "location": location,
    "duration": date_posted,
    "job_type": job_type,
    "job_status": job_status,
    "level": level,
    "years_of_experience": years_of_experience,
    "skills_required": skills_required
})

df.to_csv("wuzzuf_data_analyst.csv", index=False)