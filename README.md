# RedFlagDeals-New-Deal
Scarpy project to get the new hot deal's alarm from RedFlagDeals, send to Telegram channel by a bot.


Install scrapy: pip install scrapy
Start a new project: scrapy startproject demo
Enter the directory: cd demo
Create a new Spider: scrapy genspider rfd https://forums.redflagdeals.com/hot-deals-f9/?sk=tt&rfd_sk=tt&sd=d
Run the Spider: scrap crawl rfd


Add below files to the correct directories:
demo/config_loader.ini
demo/tg.py
demo/cron.py
demo/demo/items.py
demo/demo/spiders/rfd.py


Install apscheduler: pip install apscheduler
Start the corn job: python3 cron.py 


yum install screen
screen -dmS rfd
screen -ls
screen -r rfd