import psycopg2

from flask import Flask,request


app = Flask("Job site")

items=["python", "perl", "ruby"]

@app.route("/")
def hello():
	dbconn=psycopg2.connect("dbname=naukri")
	cur = dbconn.cursor()
	cur.execute("select title,company_name,jd_text from openings");
	ret = []
	for title,name,dsc in cur.fetchall():
		item= f"<b>{title}</b> :: {name} :: <br/> {dsc}"
		ret.append(item)
	l= "<hr/>".join(ret)
	return f"List of jobs -> <br/>{l}"
	
	
	

#http://127.0.0.1:5000/add?item=x
@app.route("/add")
def add_item():
	item = request.args.get("item")
	items.append(item)
	return f"thie list of items -> {len(items)}"
