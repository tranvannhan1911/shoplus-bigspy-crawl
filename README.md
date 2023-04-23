docker run --name crawler -d -p 8000:8000 -v ./db.sqlite3:/app/db.sqlite3 --restart always tranvannhan1911/crawl-shoplus-bigspy

exec(open("test.py").read())