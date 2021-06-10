import requests
import bs4
import sys
import psycopg2

def fetch_jobs():
	url = "https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&keyword=python&location=bangalore&k=python&l=bangalore&seoKey=python-jobs-in-bangalore&src=jobsearchDesk&latLong="

	headers={"appid" : "109",
         "systemid" : "109"}
	r = requests.get(url, headers=headers)
	data = r.json()
	return data["jobDetails"]
	
def insert_jobs(jobs):
	dbconn=psycopg2.connect("dbname=naukri")
	cur = dbconn.cursor()
	for i in jobs:
		title= i['title']
		jobid = i['jobId']
		company = i['companyName']
		url = i['jdURL']
		soup = bs4.BeautifulSoup(i['jobDescription'],features="html.parser")
		desc = str(soup.text)
		cur.execute("""INSERT INTO openings (title,job_id, company_name,jd_url, jd_text) VALUES (%s,%s,%s,%s,%s) """ , (title, jobid, company,url,desc));
		dbconn.commit()
		
		 			
def create_db():
	dbconn=psycopg2.connect("dbname=naukri")
	cur = dbconn.cursor()
	f=open("job.sql")
	sql_code=f.read()
	f.close()
	cur.execute(sql_code)
	dbconn.commit()

def main(arg):
	if arg == "create":
		create_db()
	elif arg == "crawl":
		jobs = fetch_jobs()
		insert_jobs(jobs)
	else:
		print("type create to create db, crawl to enter data to db");
			
	
if __name__ == "__main__":
	main(sys.argv[1])
	
	
	
