# o = "asdsasda"
# alpha = list(map(str,"abcdefghijklmnopqrstuvwxyz"))
# letter = "o"

# postinglist_dict_af = {'a':{ 0:[1],1:[1]}}
# postinglist_dict_gp = {'b':1}
# postinglist_dict_qz = {'c':2}

# # if(letter >= "a" and letter <="f") :
# #     postings = postinglist_dict_af
# # elif (letter >= "g" and letter <="p"):
# #     postings = postinglist_dict_gp
# # else:
# #     postings = postinglist_dict_qz


# # print(list(postinglist_dict_af["a"].keys()) in [1,2,3])

# # print(postinglist_dict_gp.update(postinglist_dict_qz))
# # print(postinglist_dict_gp)

# # switch=(letter)
# # if (letter >= "a") and (letter <="f"):
# #     print("alpha_af")
# # else: print("no")

# def update_docfreq(self,term): # Only keep relevant document freqs
#         if (term in self.document_frequency):
#             self.doc_freq[term] = self.document_frequency[term]
#         return False
#     # def gather_termfreq(self,term): # Only keep relevant term freqs
#     #     # for id in relevant_doc_ids:
#     #     #     if (term in self.posting and  id in self.posting[term]):
#     #     #         self.term_freqter


#     #     # if (term in self.posting and self.posting[term]):
#     #     #     self.temp_termfreq_ids[term]=self.posting[term]
#     #     #     ids = list(self.posting[term].keys())
#     #     #     self.termfreq_ids+=list(self.posting[term].keys())
#     #     #     frequencies = {term:[{id:self.posting[term][id][0]} for id in ids if id in self.relevant_doc_ids]}
#     #     #     self.term_freq.update(frequencies)
            

# import math
# import json
# import requests

# # we'll generate some fake texts to experiment with
# corpus = [
#     'Human machine interface for lab abc computer applications',
#     'A survey of user opinion of computer system response time',
#     'The EPS user interface management system',
#     'System and human system engineering testing of EPS',
#     'Relation of user perceived response time to error measurement',
#     'The generation of random binary unordered trees',
#     'The intersection graph of paths in trees',
#     'Graph minors IV Widths of trees and well quasi ordering',
#     'Graph minors A survey'
# ]

# # remove stop words and tokenize them (we probably want to do some more
# # preprocessing with our text in a real world setting, but we'll keep
# # it simple here)
# stopwords = set(['for', 'a', 'of', 'the', 'and', 'to', 'in'])
# texts = [
#     [word for word in document.lower().split() if word not in stopwords]
#     for document in corpus
# ]

# # build a word count dictionary so we can remove words that appear only once
# word_count_dict = {}
# for text in texts:
#     for token in text:
#         word_count = word_count_dict.get(token, 0) + 1
#         word_count_dict[token] = word_count



# class BM25:
#     """
#     Best Match 25.

#     Parameters
#     ----------
#     k1 : float, default 1.5

#     b : float, default 0.75

#     Attributes
#     ----------
#     tf_ : list[dict[str, int]]
#         Term Frequency per document. So [{'hi': 1}] means
#         the first document contains the term 'hi' 1 time.

#     df_ : dict[str, int]
#         Document Frequency per term. i.e. Number of documents in the
#         corpus that contains the term.

#     idf_ : dict[str, float]
#         Inverse Document Frequency per term.

#     doc_len_ : list[int]
#         Number of terms per document. So [3] means the first
#         document contains 3 terms.

#     corpus_ : list[list[str]]
#         The input corpus.

#     corpus_size_ : int
#         Number of documents in the corpus.

#     avg_doc_len_ : float
#         Average number of terms for documents in the corpus.
#     """

#     def __init__(self, k1=1.5, b=0.75):
#         self.b = b
#         self.k1 = k1

#     def fit(self, corpus):
#         """
#         Fit the various statistics that are required to calculate BM25 ranking
#         score using the corpus given.

#         Parameters
#         ----------
#         corpus : list[list[str]]
#             Each element in the list represents a document, and each document
#             is a list of the terms.

#         Returns
#         -------
#         self
#         """
#         tf = []
#         df = {}
#         idf = {}
#         doc_len = []
#         corpus_size = 0
#         for document in corpus:
#             corpus_size += 1
#             doc_len.append(len(document))

#             # compute tf (term frequency) per document
#             frequencies = {}
#             for term in document:
#                 term_count = frequencies.get(term, 0) + 1
#                 frequencies[term] = term_count

#             tf.append(frequencies)

#             # compute df (document frequency) per term
#             for term, _ in frequencies.items():
#                 df_count = df.get(term, 0) + 1
#                 df[term] = df_count

#         for term, freq in df.items():
#             idf[term] = math.log(1 + (corpus_size - freq + 0.5) / (freq + 0.5))

#         self.tf_ = tf
#         self.df_ = df
#         self.idf_ = idf
#         self.doc_len_ = doc_len
#         self.corpus_ = corpus
#         self.corpus_size_ = corpus_size
#         self.avg_doc_len_ = sum(doc_len) / corpus_size
#         return self

#     def search(self, query):
#         scores = [self._score(query, index) for index in range(self.corpus_size_)]
#         return scores

#     def _score(self, query, index):
#         score = 0.0

#         doc_len = self.doc_len_[index]
#         frequencies = self.tf_[index]
#         print(frequencies, "\n --------------------frequencies")

#         for term in query:
#             if term not in frequencies:
#                 continue

#             freq = frequencies[term]
#             print(term,frequencies[term], "\n ----------------------freq")
#             numerator = self.idf_[term] * freq * (self.k1 + 1)
#             denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len_)
#             score += (numerator / denominator)

#         return score
# # query our corpus to see which document is more relevant
# query = 'The intersection of graph survey and trees'
# query = [word for word in query.lower().split() if word not in stopwords]

# bm25 = BM25()
# bm25.fit(texts)
# print(bm25.tf_)
# scores = bm25.search(query)

# # for score, doc in zip(scores, corpus):
# #     score = round(score, 3)
# #     print(str(score) + '\t' + doc)

import nltk
nltk.download('tagsets')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import PunktSentenceTokenizer
k1 = 1.5
k1_increase = k1*1.2
k1_decrease = k1*0.8
pos_tags_k1={"CC": k1_decrease ,"CD":k1 ,"DT": k1_decrease ,"EX": k1_decrease ,"FW":k1,"IN": k1_decrease ,"JJ":k1_increase,"JJR":k1_increase,"JJS":k1_increase,"LS": k1_decrease ,"MD":k1,"NN":k1_increase,"NNP":k1_increase,"NNPS":k1_increase,"NNS":k1_increase,"PDT":k1,"POS": k1_decrease ,"PRP":k1_decrease ,
        "PRP$": k1_decrease ,"RB":k1,"RBR":k1,"RBS":k1,"RP": k1_decrease ,"SYM": k1_decrease,"TO": k1_decrease,"UH": k1_decrease,"VB":k1_increase,"VBD":k1_increase,"VBG":k1_increase,"VBN":k1_increase,"VBP":k1_increase,"VBZ":k1_increase,"WDT": k1_decrease,"WP": k1_decrease,"WP$": k1_decrease,"WRB": k1_decrease}

query = 'Whether you\'re new to programming or an experienced developer, it\'s easy to learn and use Python.'
query_tokenized = nltk.word_tokenize(query)   
query_k1_values = {}
query_pos_tags=nltk.pos_tag(query_tokenized)
for word in query_pos_tags:
    if len(word[0])==1: continue
    query_k1_values[word[0]] = pos_tags_k1[word[1]]

print(query_k1_values)
# increase: 1.2 decrese 0.8
