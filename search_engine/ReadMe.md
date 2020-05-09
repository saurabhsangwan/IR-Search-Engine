* Python version - Python 3.7.5
* Install requirements from requirements.txt file.
* To run application, use command - "python manage.py runserver", default port 8000.
  The application will start at "http://127.0.0.1:8000/".
* To enter django-shell, use command - "python manage.py shell"
* To crawl pages, run this code from django-shell- 
 ~~~
from crawler.WebCrawler import WebCrawler
s = WebCrawler("https://cs.uic.edu")
s.run_scraper()
 ~~~
* To create index, run this code from django-shell -
~~~
from vectorise.utils import create_index
create_index()
~~~
