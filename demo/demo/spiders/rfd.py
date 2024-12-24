import scrapy
import configparser
import tg
from demo.items import RfdItem  # Ensure RfdItem is properly defined in demo/items.py
from urllib.parse import quote


class RfdSpider(scrapy.Spider):
    name = 'rfd'
    allowed_domains = ['redflagdeals.com']
    start_urls = ['https://forums.redflagdeals.com/hot-deals-f9/?sk=tt&rfd_sk=tt&sd=d']

    def parse(self, response):
        #########################################################################
        #  Configuration
        #########################################################################
        CONFIG_FILE = 'config_loader.ini'
        CONFIG_MAIN = 'main'
        configParser = configparser.ConfigParser()
        configParser.read(CONFIG_FILE)

        # Retrieve the last processed UID from the configuration file
        try:
            old_uid = configParser.get(CONFIG_MAIN, "uid")
        except configparser.NoOptionError:
            old_uid = "0"  # Default to "0" if UID is not set

        # Initialize the maximum UID found in this scrape
        max_uid = old_uid

        #########################################################################
        #  Extract all threads from the forum page
        #########################################################################
        # Each thread is contained within an <li> element with class "topic"
        threads = response.xpath('//ul[contains(@class, "topiclist")]/li[contains(@class, "topic")]')

        for thread in threads:
            # Initialize the item to store thread data
            item = RfdItem()

            # Extract the thread UID from the data-thread-id attribute
            uid = thread.xpath('./@data-thread-id').get()
            if not uid:
                continue  # Skip if UID is not found

            item['uid'] = uid

            # Extract the retailer from the <a> tag with class "thread_dealer"
            retailer = thread.xpath('.//a[contains(@class, "thread_dealer")]/span/text()').get()
            retailer = retailer.strip() if retailer else ''

            # Extract the thread title from the <a> tag with class "thread_title_link"
            title = thread.xpath('.//h3[contains(@class, "thread_title")]/a[contains(@class, "thread_title_link")]/text()').get()
            title = title.strip() if title else ''

            # Combine retailer and title if retailer exists
            if retailer:
                final_title = f"[{retailer}] {title}"
            else:
                final_title = title

            #####################################################################
            #  Determine if the thread is new by comparing UID
            #####################################################################
            if uid > old_uid:
                # Update max_uid if the current UID is greater
                if uid > max_uid:
                    max_uid = uid

                # Encode the title for URL and message safety
                encoded_title = quote(final_title, safe='')

                # Construct the thread link using the UID
                link = f'https://forums.redflagdeals.com/viewtopic.php?t={uid}'

                # Prepare the Telegram message
                bot_message = f'*{encoded_title}*\n{link}'

                # Send the message to Telegram channel
                tg.bot_sendtext_channel(bot_message)

        #########################################################################
        #  Update the UID in the configuration file to the latest UID found
        #########################################################################
        configParser.set(CONFIG_MAIN, "uid", max_uid)
        with open(CONFIG_FILE, 'w') as configfile:
            configParser.write(configfile)