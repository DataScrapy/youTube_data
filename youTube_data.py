from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import time
from  bs4 import BeautifulSoup as soup
import pandas as pd
from datetime import datetime


def scroll_to_bottom(url, root_dir):
    try:
        options = Options()
        options.headless = True

        driver = webdriver.Firefox(service_log_path="NULL", options=options,
                                   executable_path=root_dir + "/geckodriver.exe")
        driver.get(url)
        time.sleep(10)

        old_position = 0
        new_position = None

        i = 0
        while new_position != old_position:
            # Get old scroll position
            old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
            # Sleep and Scroll
            time.sleep(3)
            driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
            # Get new position
            new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

            if i >50:
                break
            i += 1

        page_content = soup(driver.page_source, "html5lib")
        time.sleep(2)
        driver.quit()

        return page_content

    except:
        try:
            driver.quit()
        except:
            pass
        pass



def you_tube_channel(root_dir):
    try:
        print("enter the input searching for:")
        input_txt = str(input()).strip()

        url = "https://www.youtube.com/results?search_query=" +input_txt

        page_soup = scroll_to_bottom(url, root_dir)

        container = page_soup.findAll("ytd-video-renderer", {"class": "style-scope ytd-item-section-renderer"})

        channel_lst = []
        channel_dict_lst = []
        for urls in container:
            try:
                channel_link = urls.findAll("a", {"class": "yt-simple-endpoint style-scope yt-formatted-string"})
                channel_name = channel_link[0].text.strip()
                channel_link = "http://www.youtube.com" + str(channel_link[0]["href"])

                if channel_link in channel_lst:
                    continue

                dict_data = {"channel_name": channel_name, "channel_link": channel_link}
                channel_dict_lst.append(dict_data)
                channel_lst.append(channel_link)
                print(dict_data)

            except:
                pass

        file_name = datetime.now().strftime("%d%b%Y%H%M%S") + "youTube_channels.csv"
        df = pd.DataFrame(columns= ["Channel_Name", "Channel_Link"])
        for data in channel_dict_lst:
            df = df.append({"Channel_Name": data["channel_name"], "Channel_Link": data["channel_link"]}, ignore_index=True)

        df.to_csv(file_name)

    except:
        pass


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    you_tube_channel(root_dir)