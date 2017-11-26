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

    def get_google_page(self,query_arr):
        query = "+".join(query_arr)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request('http://www.google.com/search?q='+query,headers=headers)
        page = urllib.request.urlopen(req)
        html = page.read()
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

    def search_whole_question(self,question):
        query_plus = question.replace(' ','+')
        #print("query url:", "www.google.com/search?q="+query_plus)
        webbrowser.get('chrome').open_new_tab("http://www.google.com/search?q="+query_plus)

    def search_answer(self,question,ans):
        self.search_whole_question(question)
        #try quote
        # find_quote = False
        # qmark_combine = (("“","\""),("\"","\""),("“","“"),("\"","“"),("“","”"),("\"","”"),("”","“"))
        # for qc in qmark_combine:
        #     start_pt = query_plus.find(qc[0])
        #     end_pt = query_plus.find(qc[1], start_pt + 1)  # add one to skip the opening "
        #     quote = query_plus[start_pt + 1: end_pt]  # add one to get the quote excluding the ""
        #     if len(quote)!=0 and start_pt!=-1 and end_pt!=-1:
        #         print("find quote!")
        #         find_quote = True
        #         print(quote)
        #         webbrowser.get('chrome').open_new_tab("http://www.google.com/search?q="+quote)

        # #search proper nouns
        # translator = str.maketrans('', '', string.punctuation)
        # query = query.translate(translator)
        # tagged_sent = pos_tag(query.split())
        # propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
        # propernouns = list(filter(lambda x: x != "Which", propernouns))
        # if len(propernouns)!=0:
        #     if find_quote == False:
        #         print("search: "," ".join(propernouns))
        #         webbrowser.get('chrome').open_new_tab("http://www.google.com/search?q="+"+".join(propernouns))
        # print('------------------------------------------------------')
        # if len(ans)<=5:
        #     for a in ans:
        #         query_arr = [a]+propernouns
        #         print("\n"+"+".join(query_arr))
        #         url = self.google_find_first_url(query_arr)
        #         print(url)
        #         print(len(url))

        # print('------------------------------------------------------')
        # print('------------------------------------------------------')
if __name__ == '__main__':
    questions = [["Which of these websites is owned by Vice Media?",["IGN","Joystiq","Waypoint"]]]
    searcher = Searcher()
    for q in questions:
        print(q)
        searcher.search_answer(q[0],q[1])
