from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging


PATH = "C:\\Users\\gamer\\Desktop\\downloadAllEpisodesFromAnimeId\\chromedriver.exe"

s = Service(PATH)
driver = webdriver.Chrome(service=s)
BASE_URL = "https://animeid.to/ver/somali-to-mori-no-kamisama-"
EPISODES_TO_DOWNLOAD = [1, 12]


# PATH = "C:\\Users\\gamer\\Desktop\\downloadAllEpisodesFromAnimeId\\chromedriver.exe"

# BASE_URL = "https://animeid.to/ver/radiant-2nd-season-"
# EPISODES_TO_DOWNLOAD = [11, 21]
# driver = webdriver.Chrome(PATH)
logging.basicConfig(filename="whatHappened.log", level=logging.INFO)


def downloadsEpisode(currentEpisodeNumber, BASE_URL, lastEpisodeNumber):

    if (currentEpisodeNumber > lastEpisodeNumber) == False:

        # open new tab
        driver.execute_script("window.open();")
        # store window tabs in a list
        Window_List = driver.window_handles
        # switch browser focus to last tab created
        driver.switch_to.window(Window_List[-1])
        # open the url given in current tab
        driver.get(BASE_URL + str(currentEpisodeNumber))

        # Get iframe 1 - this updates DRIVER to be within that iframe
        WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "div.play-video > iframe")))

        try:

            megaLiElement = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//li[contains(text(), 'Mega')]"))
            )

        # megaLiElement = driver.find_element(By.XPATH,
        #                                     "//li[contains(text(), 'Mega')]")
        # megaLiElement = driver.find_element(By.CSS_SELECTOR,
        #                                     "ul li.linkserver:last-child")

        except:
            logging.info(
                'Error occured. Could not find megaLiElement on AnimeId.')

        finally:
            rawMegaLink = megaLiElement.get_attribute("data-video")
            megaLinkAlmostPure = rawMegaLink.replace("embed#!", "file/")
            pureMegaLink = megaLinkAlmostPure.replace("!", "#")
            driver.get(pureMegaLink)
            #   wait that element download appears then
            try:
                downloadButton = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "button.mega-button.positive.js-default-download.js-standard-download"))
                )
            except:
                logging.info(
                    'Error occured. Could not find dowload Button on Mega website. currentEpidose:' + str(currentEpisodeNumber))

            finally:
                downloadButton.click()
                downloadsEpisode(currentEpisodeNumber+1,
                                 BASE_URL, lastEpisodeNumber)
    logging.info(
        'currentEpisodeNumber > lastEpisodeNumber is true NO MORE EP TO DL')


downloadsEpisode(EPISODES_TO_DOWNLOAD[0], BASE_URL, EPISODES_TO_DOWNLOAD[1])
