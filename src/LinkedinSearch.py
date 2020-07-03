import os, time, re
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys


class LinkedinSearch:

    def __init__(self):
        self.browser = None
        self.page_range = None

    def login(self, user_id, passkey):
        path = os.getcwd() + '\src\chromedriver.exe'
        try:
            self.browser = webdriver.Chrome(executable_path=path)
        except selenium.common.exceptions.WebDriverException as err:
            raise RuntimeError('Run the program using the run.sh file in the root folder')
        self.browser.get('http://www.linkedin.com')
        sign_in = self.browser.find_element_by_class_name('nav__button-secondary')
        sign_in.click()
        time.sleep(1)
        username = self.browser.find_element_by_id('username')
        username.send_keys(user_id)
        password = self.browser.find_element_by_id('password')
        password.send_keys(passkey)
        time.sleep(0.2)
        log_in_button = self.browser.find_element_by_class_name('btn__primary--large')
        log_in_button.click()

    def checkLogin(self):
        try:
            self.browser.find_element_by_css_selector('.feed-identity-module__actor-meta')
        except selenium.common.exceptions.NoSuchElementException:
            input("Check login within browser and press Enter to continue...")

    def scanPages(self, web_address):
        self.browser.get(web_address)
        time.sleep(1)
        soup = BeautifulSoup(self.browser.page_source, "lxml")
        self.page_range = soup.select('ul.artdeco-pagination__pages li')[-1]
        self.page_range = list(range(1, int(self.page_range.select('button span')[0].get_text()) + 1))

    def scanPage(self):
        js_command = '''var lastScrollHeight = 0;
        function autoScroll() {
          var sh = document.documentElement.scrollHeight;
          if (sh != lastScrollHeight) {
            lastScrollHeight = sh;
            document.documentElement.scrollTop = sh;
          }
        }
        window.setInterval(autoScroll, 10);'''
        time.sleep(2)
        no_of_pagedowns = 20
        elem = self.browser.find_element_by_css_selector('section[aria-label="search results"] > div')
        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
            no_of_pagedowns -= 1

    def getResults(self):
        candidate = []
        for i in self.page_range:
            try:
                self.scanPage()
            except selenium.common.exceptions.NoSuchElementException:
                input('check browser before continuing')
                continue
            soup = BeautifulSoup(self.browser.page_source, "lxml")
            page_results = soup.select('ul.jobs-search-results__list > li.occludable-update')
            for result in page_results:
                res = result.select('div.artdeco-entity-lockup__title a')
                if res:
                    candidate.append("http://www.linkedin.com" + res[0].get('href'))
            if i < len(self.page_range):
                try:
                    btn = self.browser.find_element_by_css_selector('button[aria-label="Page {page}"]'.format(page=i + 1))
                    btn.click()
                except selenium.common.exceptions.NoSuchElementException:
                    self.browser.back()
                    time.sleep(2)
                    if i + 2 <= len(self.page_range):
                        btn = self.browser.find_element_by_css_selector(
                            'button[aria-label="Page {page}"]'.format(page=i + 2))
                        btn.click()
        return candidate

    def scoreJob(self, search_tag, qualification):
        dump = False
        matches = re.findall(search_tag, qualification)
        link_score = 0
        tag = {None}
        for match in matches:
            if match[3]:
                dump = True
                break
            if match[0]:
                link_score += 100
                tag.add('entry-level')
            if match[1]:
                exp = list(map(str, match[1]))
                link_score -= 50 * int(exp[0])
                tag.add('%s-workex' % exp[0])
            if match[2]:
                exp = list(map(str, match[2]))
                link_score -= 50 * int(exp[0])
                tag.add('%s-workex' % exp[0])
            if match[4]:
                link_score += 50
                tag.add(match[4])
            if match[5]:
                link_score += 20
                tag.add(match[5])
            if match[6]:
                link_score += 10
                tag.add(match[6])
            if match[7]:
                link_score += 5
                tag.add(match[5])
        return link_score, dump, tag
