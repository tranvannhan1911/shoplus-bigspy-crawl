docker run --name crawler -d -p 80:8000 -v ./db.sqlite3:/app/db.sqlite3 --restart always tranvannhan1911/socialcrawler

exec(open("test.py").read())