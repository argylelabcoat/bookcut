import mechanize
from time import sleep
from bs4 import BeautifulSoup as Soup
import requests
from downloader import file_downloader
from db_rules import file_checker
from libgen import epub_finder, file_name
import pyfiglet

def downloading(link,name,author,file):
    page = requests.get(link)
    resp = page.status_code
    soup = Soup(page.content, 'html.parser')

    searcher = [a['href'] for a in soup.find_all(href=True) if a.text]

    #print(searcher[0])
    searcher_link = searcher[0]
    file_downloader(searcher_link,name,author,file)


def book_search(name,author,publisher):
    libgen_working_url = mirror_checker()
    print("LUBGEN", libgen_working_url)
    file_exists = file_checker(name,author)
    if file_exists is True:
        print('File already exists in Collection!\n' + "=====================================\n")
    else:
            br = mechanize.Browser()
            br.set_handle_robots(False)   # ignore robots
            br.set_handle_refresh(False)  #
            br.addheaders = [('User-agent', 'Firefox')]


            url = "http://libgen.li/"
            response = br.open(url)
            br.select_form('libgen')
            input_form = name + ' ' + author
            br.form['req'] = input_form
            ac = br.submit()
            html_from_page = ac
            soup = Soup(html_from_page,'html.parser')


            #href = soup.find_all(title = "libgen",href = True)
            try:
                line_with_epub = epub_finder(soup)
                links_with_text = [a['href'] for a in soup.find_all(title = "libgen", href=True) if a.text]
                Downloading_page = links_with_text[line_with_epub]
                print("\nDownloading Link: FOUND")
                print(Downloading_page)
                nameofbook = file_name(Downloading_page)
                downloading(Downloading_page,name,author,nameofbook)
            except IndexError:
                print("\nDownloading Link:  NOT FOUND")
                pass
            print ("================================ \n")
            br.close()

def custom_download():
    title= pyfiglet.figlet_format("BookCut")
    print("**********************************",'\n',title,'\n', "**********************************")

    print("Welcome to BookCut!  I'm here to help you \n to read your favourite books! \n")
    name = input("Name of Book: ")
    author = input("Author: ")
    book_search(name,author,"")

def mirror_checker():
    mirrors = ['http://libgen.li/', 'https://libgen.is/', 'https://Libgen.me/',
    'http://gen.lib.rus.ec/', 'https://Libgen.unblockit.id/', 'http://Libgen.unblocked.pet']
    for i in mirrors:
        try:
            response = br.open(i)
            r_url = response.geturl()
            if i == r_url:
                return i
                print("HEY" , i)
                break
            else:
                print("No mirrors available")
        except:
            pass