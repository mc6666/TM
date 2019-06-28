from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import krovetz

def scrap_keywords():
    stemmer = krovetz.PyKrovetzStemmer()
    # keyword_list_TERM： {key:{converted_word, count}}
    keyword_list_TERM={}
    html_page = urlopen("https://en.wikipedia.org/wiki/List_of_Microsoft_software")
    soup = BeautifulSoup(html_page, features="lxml")
    div = soup.find('div', attrs={'id': 'mw-content-text'})
    footer = str(div.contents).rfind("Misc.")

    for link in div.findAll('a', attrs={'href': re.compile("/wiki/")}): #"^https://")}):
        link_text = link.text.replace('+','').lower().strip()
        # lemmatize
        link_text=stemmer.stem(link_text)
        #if link_text=='Microsoft Edge'.lower():
        #    print(stemmer.stem(link_text))
        if link_text in keyword_list_TERM.keys():
            keyword_list_TERM[link_text]['count']+=1
        else:
            keyword_list_TERM[link_text]={'converted_word':link_text.replace(" ", "_")}
            keyword_list_TERM[link_text]['count']=1

        link_text = link.text.replace('+','').lower().replace('microsoft', 'ms').strip()
        # lemmatize
        link_text=stemmer.stem(link_text)
        if link_text in keyword_list_TERM.keys():
            keyword_list_TERM[link_text]['count']+=1
        else:
            keyword_list_TERM[link_text]={'converted_word':link_text.replace(" ", "_")}
            keyword_list_TERM[link_text]['count']=1

        link_text = link.text.replace('+','').lower().replace('microsoft', '').strip()
        # lemmatize
        link_text=stemmer.stem(link_text)
        if link_text in keyword_list_TERM.keys():
            keyword_list_TERM[link_text]['count']+=1
        else:
            keyword_list_TERM[link_text]={'converted_word':link_text.replace(" ", "_")}
            keyword_list_TERM[link_text]['count']=1
            
        #print (link_text)
        if link_text == 'Windows To Go'.lower(): 
            break

    link_text= 'window'       
    if link_text in keyword_list_TERM.keys():
        keyword_list_TERM[link_text]['count']+=1
    else:
        keyword_list_TERM[link_text]={'converted_word':link_text}
        keyword_list_TERM[link_text]['count']=1
    key_list=list(keyword_list_TERM.keys())


    for key1 in key_list:
        if key1.startswith('list of '):
            del keyword_list_TERM[key1]

    # get Ubuntu Glossaries
    html_page = urlopen("https://help.ubuntu.com/community/Glossary")
    soup = BeautifulSoup(html_page, features="lxml")
    for link in soup.findAll('p', attrs={'class': re.compile("^line")}): #"^https://")}):
        strong_tag = link.find('strong')
        if not strong_tag == None:
            strong_tag_text = strong_tag.text.lower().strip()
            strong_tag_text=stemmer.stem(strong_tag_text)
            if strong_tag_text == 'Contributors:'.lower():
                break
            if strong_tag_text.find('(or') >= 0 and strong_tag_text.endswith(')'):
                #print('two_glossary={}'.format(strong_tag_text))
                two_glossary = strong_tag_text.split('(or')
                for item in two_glossary:
                    item=item.strip().replace(")", '')
                    item=stemmer.stem(item)
                    if item in keyword_list_TERM.keys():
                        keyword_list_TERM[item]['count']+=1
                    else:
                        keyword_list_TERM[item]={'converted_word':item.replace(" ", "_")}
                        keyword_list_TERM[item]['count']=1
            else:    
                if strong_tag_text.find('(also') >= 0 :
                    strong_tag_text=strong_tag_text[:strong_tag_text.find('(also')]
                strong_tag_text=strong_tag_text
                if strong_tag_text.find('ubuntu') >= 0 :
                    strong_tag_text='ubuntu'
                if strong_tag_text in keyword_list_TERM.keys():
                    keyword_list_TERM[strong_tag_text]['count']+=1
                else:
                    keyword_list_TERM[strong_tag_text]={'converted_word':strong_tag_text.replace(" ", "_")}
                    keyword_list_TERM[strong_tag_text]['count']=1
            #print (strong_tag_text)

    print(len(keyword_list_TERM.keys()))
    # Save Keywords
    import pickle
    with open("keyword_list.pickle", 'wb') as f:
        pickle.dump(keyword_list_TERM, f)
        
if __name__ == "__main__":
    scrap_keywords()        