import webbrowser
from nltk.tag import pos_tag
import string
import urllib

class Searcher:
    def __init__(self):
        pass

    # def alexa_rank(self,url):
    #     xml = request.urlopen('http://data.alexa.com/data?cli=10&dat=s&url=%s'%url).read().decode("utf-8")
    #     sp = re.search(r'REACH RANK="\d+"', xml).span()
    #     return int(xml[sp[0]+12:sp[1]-1])

    def get_page(self,query):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request('http://www.google.com/search?q='+query,headers=headers)
        page = urllib.request.urlopen(req)
        html = page.read()
        return html

    def search_answer(self,query,ans):
        #search whole question
        query_plus = query.replace(' ','+')
        #print("query url:", "www.google.com/search?q="+query_plus)
        webbrowser.get('chrome').open_new_tab("http://www.google.com/search?q="+query_plus)

        #try quote
        find_quote = False
        qmark_combine = (("“","\""),("\"","\""),("“","“"),("\"","“"),("“","”"),("\"","”"),("”","“"))
        for qc in qmark_combine:
            start_pt = query_plus.find(qc[0])
            end_pt = query_plus.find(qc[1], start_pt + 1)  # add one to skip the opening "
            quote = query_plus[start_pt + 1: end_pt]  # add one to get the quote excluding the ""
            if len(quote)!=0 and start_pt!=-1 and end_pt!=-1:
                print("find quote!")
                find_quote = True
                print(quote)
                webbrowser.get('chrome').open_new_tab("http://www.google.com/search?q="+quote)

        #search proper nouns
        translator = str.maketrans('', '', string.punctuation)
        query = query.translate(translator)
        tagged_sent = pos_tag(query.split())
        propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
        propernouns = list(filter(lambda x: x != "Which", propernouns))
        if len(propernouns)!=0:
            if find_quote == False:
                print("search: "," ".join(propernouns))
                webbrowser.get('chrome').open_new_tab("http://www.google.com/search?q="+"+".join(propernouns))
        print('------------------------------------------------------')
        if len(ans)<=5:
            for a in ans:
                print("\n"+a+" "+" ".join(propernouns))
                try:
                    html=self.get_page(a+"+"+"+".join(propernouns))
                    html = str(html)
                    start_idx = html.find("<h3 class=\"r\"><a href=\"")
                    end_idx = html.find('\"',start_idx+len("<h3 class=\"r\"><a href=\""))
                    url = html[start_idx+len("<h3 class=\"r\"><a href=\""):end_idx]
                    print(url)
                    print(len(url))
                except:
                    pass
        print('------------------------------------------------------')
        print('------------------------------------------------------')
