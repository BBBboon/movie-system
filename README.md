# Movie System #

### technology stack ###
Django, matplotlib, MySQL, HTML, CSS, JavaScript, SnowNLP

### project description ### 
I crawled the Douban Top 250 movie information and collected 50,000 movie reviews using Python. Using the Django framework, I built a system that utilizes SnowNLP with plain Bayes as a 
mathematical model for text sentiment analysis of user movie reviews. The system generates charts and provides relevant suggestions to help users quickly understand movies.

### how to use ###
1. input `python manage.py runserver` to start movie system
2. input `http://127.0.0.1:8000/home/` into your browser
3. if you want to use management system to manage user information, you can choose log up as manager after moving your mouse to the top right corner of the page

### what system can do ###
hot movies wordcloud · sentiment analysis · movies information and comments from douban · grouph visualization

### documents introduction ###
* `system`: codes(Django) to build movie system.
* `spider`: codes to crawl movies information from douban
* `media`: store pictures about system
* `employee_mgr`: Django’s configuration information
