import requests
import os
from os.path import basename
from bs4 import BeautifulSoup
 
path = os.getcwd()
print ("The current working directory is %s" % path)
 
url = 'https://scryfall.com/sets'
r=requests.get(url).text
soup = BeautifulSoup(r, 'html.parser')
 
####################GATHERS ALL URLS FROM SET DIRECTORY#####################
links = []
Urls = []
for link in soup.findAll('a'):
    links.append(link.get('href'))
 
for link in links:
    if link != None:
        if 'https://scryfall.com/sets/' in link:
            if link not in Urls:
                Urls.append(link)
 
#################START OF ALL URL LOOPS################################
for Url in Urls: ##goes threw all the URLS gathered from the sets links
    r=requests.get(Url).text
    soup = BeautifulSoup(r, 'html.parser')
 
    temp = soup.find('h1', {'class': 'set-header-title-h1'}).contents
    temp = ''.join(temp)
    temp = temp.strip()
    temp = temp.replace('"', "").replace('?', '').replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('<', '').replace('>','') 
 
    test2 = (f"{path}\\{temp}")
#############################################MAKE DIRECTORY FOR SET FOLDERS##################
    try:
        os.mkdir(test2)
    except OSError:
        print ("Creation of the directory %s failed" % test2)
    else:
        print ("Successfully created the directory %s " % test2)
 
############################################GATHER ALL IMAGES####################
    images = soup.find_all('img')
 
    pictures = [] ##stores all the picture URLS
    names = [] ##stores all the name
    nameCounter = 0
    for image in images[:-1]:
        tempname = image.get('alt')
        tempname = tempname.replace('"', "").replace('?', '').replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('<', '').replace('>','')
 
        while tempname in names:
            nameCounter += 1
            tempname = (tempname + str(nameCounter))
        else:
            names.append(tempname)
            nameCounter = 0
 
 
        if image.get('src') == None or image.get('src') == '':
            pictures.append(image.get('data-src'))
        else:
            pictures.append(image.get('src'))
    print(f"{len(pictures)} Cards in {temp}")

####################SAVES ALL IMAGES AS FILES#################
    x=0
    for i in pictures:
        fn = names[x] + '.png'
        try:
            if os.path.exists(f'{test2}\\'+basename(fn)) == False:
                with open(f'{test2}\\'+basename(fn),"wb") as f:
 
                    f.write(requests.get(i).content)
                    f.close
                    print(f"{x}/{len(pictures)} saved from {temp}")
                    x+=1
            else:
                pass
        except OSError:
            print(f"Failed to save image {fn} from set {test2} with url {i}")
            print(len(pictures))
            print(len(names))
##################RESETS IMAGES AND NAMES FOR NEXT SET FOLDER#############
 
    pictures.clear()
    names.clear()
    nameCounter = 0
print("Completed With No Errors")




	


	


