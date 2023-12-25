import json
import math
import nltk
from nltk.tokenize import PunktSentenceTokenizer
class BestMatch25: 
    def __init__(self, query,relevant_doc_ids, k1=1.5, b=0.75):
        self.b = b
        self.k1 = k1
        self.k1_increase = self.k1*1.2
        self.k1_decrease = self.k1*0.8
        self.pos_tags_k1={"CC": self.k1_decrease ,"CD":self.k1 ,"Determiner": self.k1_decrease ,"EX": self.k1_decrease ,"FW":self.k1,"IN": self.k1_decrease ,"JJ":self.k1_increase,"JJR":self.k1_increase,"JJS":self.k1_increase,"LS": self.k1_decrease ,"MD":self.k1,"NN":self.k1_increase,"NNP":self.k1_increase,"NNPS":self.k1_increase,"NNS":self.k1_increase,"PDT":self.k1,"POS": self.k1_decrease ,"PRP":self.k1_decrease ,
        "PRP$": self.k1_decrease ,"RB":self.k1,"RBR":self.k1,"RBS":self.k1,"RP": self.k1_decrease ,"SYM": self.k1_decrease,"TO": self.k1_decrease,"UH": self.k1_decrease,"VB":self.k1_increase,"VBD":self.k1_increase,"VBG":self.k1_increase,"VBN":self.k1_increase,"VBP":self.k1_increase,"VBZ":self.k1_increase,"WDT": self.k1_decrease,"WP": self.k1_decrease,"WP$": self.k1_decrease,"WRB": self.k1_decrease}
        
        self.query = nltk.word_tokenize(query)   
        self.query_pos_tags=nltk.pos_tag(self.query) # Get speech tags for querry
        self.query_k1_values = {} # Assign appropriate k1 value to token in querry based off of speech codes
        for word in self.query_pos_tags:
            if len(word[0])==1: continue
            self.query_k1_values[word[0]] = self.pos_tags_k1[word[1]]

        self.relevant_doc_ids = set(relevant_doc_ids) #list of document ideas
        self.idf={}

        with open("documentFrequency_nostem_stop.json", "r") as documents:
            self.document_frequency = json.load(documents) 

        with open("cleanDocsDict_nostem_stop.json", "r") as documents:
            self.corpus = json.load(documents)   
        self.corpus_size = len(self.corpus)
        self.average_doclen =  sum([len(doc) for doc in self.corpus])/self.corpus_size

        with open("postingListDict_nostem_stop.json", "r") as documents:
            self.posting = json.load(documents)
        

    def calculate_idf(self,term):
        if term in self.document_frequency:
            df = self.document_frequency[term]
            self.idf[term] = math.log(1 + (self.corpus_size - df + 0.5) / (df + 0.5))

    def load_idf(self):
        list(map(self.calculate_idf,self.query))
    
    def fit(self):
        bm25.load_idf() #load up idf calculations
        scores = [self.score(doc_id) for doc_id in self.relevant_doc_ids]
        return scores

    def score(self,relevant_doc):
        result = 0.0
        doc_length = len(self.corpus[relevant_doc])
        for term in self.query:
            if term in self.posting and relevant_doc in self.posting[term]: # check if term is in list of relevant docs
                freq = self.posting[term][relevant_doc][0] # term freq for doc 
                numerator = self.idf[term] * freq * (self.k1+1)
                denominator = freq + self.query_k1_values[term] * (1.0-self.b+self.b*doc_length/self.average_doclen)
                result += (numerator / denominator)
            else: continue
        return [relevant_doc,result]


bm25 = BestMatch25("james bond wii calculus",['150035', '1065834', '554919', '406512', '5944391', '61849', '14880785', '209050', '1524064', '2152689', '347422', '108391', '49030177', '2887318', '18207983', '1512303', '7035425', '46782188', '1872229', '1065834', '554919', '13268827', '406512', '939401', '15275379', '1588966', '61849', '14880785', '7723568', '511793', '585215', '166705', '876126', '24919289', '310301', '347422', '4781915', '2887318', '18207983', '300445', '1213194', '1512303', '1168659', '1290848', '215764', '73423', '1872229', '1065834', '197982', '406512', '5944391', '74596', '61849', '1357871', '209050', '511793', '151408', '585215', '1426096', '5921039', '2051778', '104066', '310301', '347422', '18207983', '319022', '1512303', '706315']) #relevant doc ids = the ids in the small sample of documents from the json file (ALL OF THEM. Thats why there are some zeros in the results).
scores = bm25.fit()
print(scores)
print(bm25.query)
# for i in scores:
#     print(round(i[1],4),"-------\n",bm25.corpus[i[0]][:1000],"\n----------")

class BestMatch25:
    def __init__(
        self,
        query,
        unstemmed_query,
        relevant_doc_ids,
        postings,
        document_frequencys,
        corpus_info,
        k1=1.5,
        b=0.75
    ):
        self.query = query
        self.k1_increase = self.k1*1.2
        self.k1_decrease = self.k1*0.8
        self.pos_tags_k1={"CC": self.k1_decrease ,"CD":self.k1 ,"Determiner": self.k1_decrease ,"EX": self.k1_decrease ,"FW":self.k1,"IN": self.k1_decrease ,"JJ":self.k1_increase,"JJR":self.k1_increase,"JJS":self.k1_increase,"LS": self.k1_decrease ,"MD":self.k1,"NN":self.k1_increase,"NNP":self.k1_increase,"NNPS":self.k1_increase,"NNS":self.k1_increase,"PDT":self.k1,"POS": self.k1_decrease ,"PRP":self.k1_decrease ,
        "PRP$": self.k1_decrease ,"RB":self.k1,"RBR":self.k1,"RBS":self.k1,"RP": self.k1_decrease ,"SYM": self.k1_decrease,"TO": self.k1_decrease,"UH": self.k1_decrease,"VB":self.k1_increase,"VBD":self.k1_increase,"VBG":self.k1_increase,"VBN":self.k1_increase,"VBP":self.k1_increase,"VBZ":self.k1_increase,"WDT": self.k1_decrease,"WP": self.k1_decrease,"WP$": self.k1_decrease,"WRB": self.k1_decrease}
        
        self.query_tokenized = nltk.word_tokenize(unstemmed_query)   
        self.query_pos_tags=nltk.pos_tag(self.query_tokenized) # Get speech tags for querry
        self.query_unstemmed_lst = unstemmed_query.split(" ") 

        self.query_k1_values = {} # Assign appropriate k1 value to token in querry based off of speech codes
        for word in self.query_pos_tags:
            if len(word[0])==1: continue
            self.query_k1_values[word[0]] = self.pos_tags_k1[word[1]]
        
        self.relevant_doc_ids = relevant_doc_ids
        self.postings = postings
        self.document_frequencys = document_frequencys
        self.corpus_size = corpus_info["doc_count"]
        self.average_doclen = corpus_info["total_length"]/self.corpus_size
        self.corpus_lengths = corpus_info["doc_lengths"]
        self.k1 = k1
        self.b = b
        self.idf = {}

    def calculate_idf(self, term):
        if term in self.document_frequencys:
            df = self.document_frequencys[term]
            self.idf[term] = math.log(
                1 + (self.corpus_size - df + 0.5) / (df + 0.5))

    def load_idf(self):
        list(map(self.calculate_idf, self.query))

    def fit(self):
        self.load_idf()  # load up idf calculations
        scores = [self.score(doc_id) for doc_id in self.relevant_doc_ids]
        return scores

    def score(self, relevant_doc):
        result = 0.0
        doc_length = self.corpus_lengths[relevant_doc]
        for i in range(len(self.query)):
            term=self.query[i]
            term_unstemmed = self.query_unstemmed_lst[i]
            # check if term is in list of relevant docs
            if term in self.postings and relevant_doc in self.postings[term]:
                # term freq for doc
                freq = self.postings[term][relevant_doc][0]
                numerator = self.idf[term] * freq * (self.k1+1)
                denominator = freq + self.k1 * \
                    (1.0-self.b+self.b*doc_length/self.average_doclen)
                result += (numerator / denominator)
            else:
                continue
        return [relevant_doc, result]


# bm25 = BestMatch25("james bond wii calculus",['150035', '1065834', '554919', '406512', '5944391', '61849', '14880785', '209050', '1524064', '2152689', '347422', '108391', '49030177', '2887318', '18207983', '1512303', '7035425', '46782188', '1872229', '1065834', '554919', '13268827', '406512', '939401', '15275379', '1588966', '61849', '14880785', '7723568', '511793', '585215', '166705', '876126', '24919289', '310301', '347422', '4781915', '2887318', '18207983', '300445', '1213194', '1512303', '1168659', '1290848', '215764', '73423', '1872229', '1065834', '197982', '406512', '5944391', '74596', '61849', '1357871', '209050', '511793', '151408', '585215', '1426096', '5921039', '2051778', '104066', '310301', '347422', '18207983', '319022', '1512303', '706315']) #relevant doc ids = the ids in the small sample of documents from the json file (ALL OF THEM. Thats why there are some zeros in the results).
# scores = bm25.fit()

# print(bm25.query)
# for i in scores:
#     print(round(i[1],4),"-------\n",bm25.corpus[i[0]][:1000],"\n----------")
