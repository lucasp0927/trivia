import webbrowser
from nltk.tag import pos_tag
import nltk
import string
import urllib
from unidecode import unidecode
import wikipedia
import re
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class Searcher:
    def __init__(self):
        self.google_banned = False
        self.stopwords = set(nltk.corpus.stopwords.words("english"))
        self.stopwords.add('which')
        self.stopwords.add('Which')
        self.stopwords.add('What?')
        self.stopwords.add('what?')
        self.stopwords.add('from?')
        self.stopwords.add('In')
    # def alexa_rank(self,url):
    #     xml = request.urlopen('http://data.alexa.com/data?cli=10&dat=s&url=%s'%url).read().decode("utf-8")
    #     sp = re.search(r'REACH RANK="\d+"', xml).span()
    #     return int(xml[sp[0]+12:sp[1]-1])

    def get_page(self,url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
#        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5'}
#        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        req = urllib.request.Request(url,headers=headers)
        page = urllib.request.urlopen(req)
        html = page.read()
        return html

    def get_google_page(self,query_arr):
        query = "+".join(query_arr)
        url = 'http://www.google.com/search?q='+query
        html = self.get_page(url)
        return html

    def google_find_first_url(self,query_arr):
        try:
            html= self.get_google_page(query_arr)
            html = str(html)
            start_idx = html.find("<h3 class=\"r\"><a href=\"")
            end_idx = html.find('\"',start_idx+len("<h3 class=\"r\"><a href=\""))
            url = html[start_idx+len("<h3 class=\"r\"><a href=\""):end_idx]
            return url
        except:
            return ""

    def get_first_wiki_url(self, propernouns,use_google=True):
            url = ""
            if use_google and not(self.google_banned):
                try:
                    html= self.get_google_page(propernouns+['site:wikipedia.org'])
                    html = str(html)
                    start_idx = html.find("<h3 class=\"r\"><a href=\"")
                    end_idx = html.find('\"',start_idx+len("<h3 class=\"r\"><a href=\""))
                    url = html[start_idx+len("<h3 class=\"r\"><a href=\""):end_idx]
                except:
                    self.google_banned = True
                    print("Banned by google, fallback to wikipedia.")
                    url = ""
            if len(url) == 0:
                try:
                    url = wikipedia.page(wikipedia.search(" ".join(propernouns))[0]).url
                except:
                    url = ""
            return url

    def search_google(self,question, open_in_browser=False):
        query_plus = question.replace(' ','+')
        print("query url:", "www.google.com/search?q="+query_plus)
        if open_in_browser:
            webbrowser.get('chrome').open_new_tab("http://www.google.com/search?q="+query_plus)

    def search_quote(self,question, open_in_browser=False):
        find_quote = False
        #        qmark_combine = (("“","\""),("\"","\""),("“","“"),("\"","“"),("“","”"),("\"","”"),("”","“"))
        qmark_combine = (("\"","\""),)
        for qc in qmark_combine:
            start_pt = question.find(qc[0])
            end_pt = question.find(qc[1], start_pt + 1)
            quote = question[start_pt + 1: end_pt]
            if len(quote)!=0 and start_pt!=-1 and end_pt!=-1:
                print("find quote!")
                find_quote = True
                print(quote)
                if open_in_browser:
                    query_plus = quote.replace(' ','+')
                    webbrowser.get('chrome').open_new_tab("http://www.google.com/search?q="+query_plus)
        return find_quote, quote

    def get_propernouns(self,question):
        find_quote, quote = self.search_quote(question)
        if find_quote:
            return quote.split()
        #search proper nouns
        translator = str.maketrans('', '', string.punctuation)
        query = question.translate(translator)
        tagged_sent = pos_tag(query.split())
        propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
        propernouns = list(filter(lambda x: x != "Which", propernouns))
        if len(propernouns) == 0:
            propernouns = list(filter(lambda t: t not in self.stopwords, query.split()))
        return propernouns

    def get_first_google_url_length(self, propernouns, ans):
        for a in ans:
            query_arr = [a]+propernouns
            print("\n"+"+".join(query_arr))
            url = self.google_find_first_url(query_arr)
            print(url)
            print(len(url))

    def find_occurance(self, text, target):
        regex = re.compile('[^0-9a-zA-Z]'+target+'[^0-9a-zA-Z]')
        match = re.findall(regex, text)
        return len(match)

    def search_wikipedia(self, propernouns, ans, use_google = True):
        print(bcolors.FAIL+"Search Wikipedia"+bcolors.ENDC)
        wiki_url = self.get_first_wiki_url(propernouns,use_google)
        print(wiki_url)
        if len(wiki_url)>0:
            html = str(self.get_page(wiki_url))
            for a in ans:
                print(a,": ", self.find_occurance(html.upper(),a.upper()))#TODO: only find term start with non-alphebatic

    def search_wikipedia2(self, question, ans, use_google = True):
        print(bcolors.FAIL+"Search Wikipedia (method 2)"+bcolors.ENDC)
        q_terms = question.lower().split(" ")
        q_terms = list(filter(lambda t: t not in self.stopwords, q_terms))
        print(q_terms)
        for a in ans:
            count = 0
            wiki_url = self.get_first_wiki_url(a.split(),use_google)
            print(wiki_url)
            if len(wiki_url)>0:
                html = str(self.get_page(wiki_url))
                for q in q_terms:
                    count += self.find_occurance(html.upper(), q.upper())/len(html)
                print(a,": ",round(count*100000))

    def search_answer(self,question,ans):
        #self.find_occurance("a aa a","a")
        question  = unidecode(question) #convert all symbol to ascii, ie: curly quote to simple quote
        self.search_google(question,False)
        propernouns = self.get_propernouns(question)
        print(propernouns)
        translator = str.maketrans('', '', string.punctuation)
        if len(propernouns)>0:
            self.search_google(" ".join(propernouns),False)
            self.search_wikipedia(propernouns, ans, True)
            question = question.translate(translator)
            self.search_wikipedia2(question, ans, True)
        print(bcolors.FAIL+"Ready to Capture!"+bcolors.ENDC)

if __name__ == '__main__':
    questions = [["Which of these websites is owned by Vice Media?",["IGN","Joystiq","Waypoint"]],
                 # ["Which 80s song begins, “Bass, how low can you go?”",["My Adidas","Push It","Bring The Noise"]],
                 # ["Which of these is a popular anime series by Rooster Teeth?",["RWBY","BURY","WAKY"]],
                 # ["In Mexico, a saladito is always known as what?",["Taco salad", "Salted plum", "Guava roll"]],
                 # ["Which actor turned down the role of James Bond twice before finally accepting",["Timothy Dalton", "Roger Moore", "Sean Connery"]],
                 # ["Which country is Bond girl actress Eva Green from?",["France", "Denmark", "England"]],
                 ["What company built the ﬁrst mobile phone?",["Motorola","Nokia","Ericsson"]]]
    searcher = Searcher()
    for q in questions:
        print("\nQuestion:\n",q)
        searcher.search_answer(q[0],q[1])
