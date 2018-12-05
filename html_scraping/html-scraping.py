# SCRAPING on fire department page

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

def test(urlll):
    
    good_urls = []
    bad_urls = []
    
    context = ssl._create_unverified_context()

    html = urlopen(urlll,context=context).read().decode('utf-8',"ignore")
    soup = BeautifulSoup(html, features='lxml')

    for tag in soup.find_all('a'):
        url = tag.get('href',None)

        if isinstance(url,type(None)):
            continue
        elif url.find('http') != -1:
            try:
                response=urlopen(url,context=context)
                good_urls.append(url)
            except:
                print("--------------\nError!!!")
                print("Title: ", tag.get_text())
                print(url)
                bad_urls.append(url)
            else:
                response.close()

    
    return good_urls, bad_urls


if __name__ == '__main__':
    
    url_string = input("Please input the url you would like to search:")

    #Search the home page
    good_urls1, bad_urls1 = test(url_string)

    #Search the next page
    for i in range(len(good_urls1)):
        url = good_urls1[i]
        print("***************\n Link {} {}\n***************\n".format(i, url))
        a,b = test(url)


