import os, sys, requests, time, csv
from bs4 import BeautifulSoup
from LinkedinSearch import LinkedinSearch
from User import User
from tagger import tagRegrex

'''

'''
if __name__ == "__main__":
    t1 = time.time()
    ls = LinkedinSearch()
    position = str(input('Enter your desired position (Default Recommended Jobs): '))
    age = int(input('Posted "x" days ago Enter x: '))*24*3600
    if position:
        web_address = 'http://www.linkedin.com/jobs/search/?f_E=2&f_JT=F&f_TPR=r'+str(age)+'&keywords=' + \
        '%20'.join(position.split())
    else:
        web_address = 'https://www.linkedin.com/jobs/search/?pivotType=jymbii'
    user = User()
    last = 'n'
    if os.path.isfile('./src/.res/user.json'):
        last = input('Login with last saved user? (Y): ')
    if last.strip().lower() in ['y', 'yes']:
        username, password = user.loadUser()
    elif last.strip().lower() in ['n','no']:
        username, password = user.createUser()
        user.saveUser()
    ls.login(username, password)
    time.sleep(0.5)
    ls.checkLogin()
    print('Login Successful')
    ls.scanPages(web_address)
    # Getting all search results
    candidate = ls.getResults()
    print('Results scraped: ', len(candidate))
    ls.browser.close()
    # Analyzing profiles
    print('Starting Analysis')
    sys.stdout.flush()
    search_tag = tagRegrex(position)
    link_scores = []
    link = []
    company = []
    position = []
    link_tags = []
    links = []
    for link in candidate:
        dump = False
        link_score = 0
        html_content = None
        # Setup HTML for littlesoup
        try:
            html_content = requests.get(link)
            html_content.raise_for_status()
        except requests.exceptions.ConnectionError:
            time.sleep(16)
            html_content = requests.get(link)
            html_content.raise_for_status()
        except requests.exceptions.HTTPError:
            continue
        little_soup = BeautifulSoup(html_content.text, 'lxml')
        details = little_soup.select('div.topcard__content-left')
        try:
            qualification = little_soup.select('div.show-more-less-html__markup')[0].get_text()
            link_score, dump, tag = ls.scoreJob(search_tag, qualification)
        except:
            qualification = ''
        if dump:
            continue
        links.append(link)
        link_scores.append(link_score)
        tag.remove(None)
        if len(tag) != 0:
            link_tags.append(','.join(tag))
        else:
            link_tags.append(None)
        try:
            company.append(details[0].select('span.topcard__flavor a')[0].get_text())
        except:
            company.append(None)
        try:
            position.append(details[0].select('h1.topcard__title')[0].get_text())
        except:
            position.append(None)

    if not os.path.isdir(os.getcwd()+'\output'):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)

    with open('./output/JobLinks.csv', 'w', newline='') as csv_file:
        write = csv.writer(csv_file, delimiter=',')
        write.writerow(('Company', 'Position', 'Link', 'Score', 'Tags'))
        write.writerows(zip(company, position, links, link_scores, link_tags))
    print('Job completed in %d seconds' % (time.time() - t1))
    input('press Enter to exit program')
