import porterAlgo

import time
import orjson
import math


class BestMatch25:
    def __init__(
        self,
        query,
        relevant_doc_ids,
        postings,
        document_frequencys,
        corpus_info,
        corpus_path,
        k1=1.5,
        b=0.75
    ):
        self.query = query
        # self.relevant_doc_ids = set(relevant_doc_ids)  # list of document ideas
        self.relevant_doc_ids = relevant_doc_ids
        self.postings = postings
        self.document_frequencys = document_frequencys
        self.corpus_size = corpus_info["doc_count"]
        self.average_doclen = corpus_info["total_length"]/self.corpus_size
        self.corpus_lengths = corpus_info["doc_lengths"]
        self.k1 = k1
        self.b = b
        #noun, verb fine, #preoposition questions words
        self.idf = {}

        # If we decide to add the first few words
        # with open(corpus_path, "rb") as documents:
        #     self.corpus = orjson.loads(documents.read())

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
        for term in self.query:
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
        # return [relevant_doc, result, " ".join(self.corpus[relevant_doc].split(" ")[:30])]


class Query:
    postings = {}
    freqs = {}
    titles = {}
    cleaned_docs = {}
    corpus_info = {}

    def __init__(
        self
    ):
        self.stopwords_on = None
        self.stem_on = None
        self.title_file_name = "docTitleDict"
        self.posting_file_name = "postingListDict"
        self.df_file_name = "documentFrequency"
        self.clean_docs_file_name = "cleanDocsDict"
        self.ci_file_name = "size"
        self.names = ["a-e", "f-j", "k-o",
                      "p-t", "u-z", "num"]
        self.porter_stemming = porterAlgo.PorterStemmer()

    def get_extension(self):
        # Get correct File Path Extension
        if self.stem_on:
            extension = "_stem"
        else:
            extension = "_nostem"
        if self.stopwords_on:
            extension += "_stop"
        else:
            extension += "_nostop"
        return extension

    def char_to_index(self, letter):
        match ord(letter):
            case letter if ord("a") <= letter <= ord("e"):
                file = 0
            case letter if ord("f") <= letter <= ord("j"):
                file = 1
            case letter if ord("k") <= letter <= ord("o"):
                file = 2
            case letter if ord("p") <= letter <= ord("t"):
                file = 3
            case letter if ord("u") <= letter <= ord("z"):
                file = 4
            case _:
                file = 5
        return file

    def load_postings_range(self, letter):
        extension = self.get_extension()
        self.postings = {}
        i = self.char_to_index(letter)
        with open(extension[1:]+"/"+self.posting_file_name+extension+"/"+self.names[i]+".json", "rb+") as postings:
            self.postings = orjson.loads(postings.read())

    # IGNORE
    def load_cd(self):
        extension = self.get_extension()
        # if not self.cleaned_docs:
        #     with open(extension[1:]+"/"+self.clean_docs_file_name+extension+".json", 'rb') as clean:
        #         self.cleaned_docs = orjson.loads(clean.read())
        return extension[1:]+"/"+self.clean_docs_file_name+extension+".json"

    def load_df(self):
        extension = self.get_extension()
        if not self.freqs:
            with open(extension[1:]+"/"+self.df_file_name+extension+".json", 'rb') as freqs:
                self.freqs = orjson.loads(freqs.read())

    def load_dt(self):
        extension = self.get_extension()
        if not self.titles:
            with open(extension[1:]+"/"+self.title_file_name+extension+".json", 'rb') as titles:
                self.titles = orjson.loads(titles.read())

    def load_ci(self):
        extension = self.get_extension()
        if not self.corpus_info:
            print(extension[1:]+"/"+self.ci_file_name+extension+".json")
            with open(extension[1:]+"/"+self.ci_file_name+extension+".json", 'rb') as corpus_info:
                self.corpus_info = orjson.loads(corpus_info.read())

    def get_window(self, size, index, doc):
        # Gets size terms to left and right of index
        if index < size:
            window = doc[:index + size + 1]
        else:
            window = doc[index-size:index + size + 1]
        return " ".join(window)

    def remove_invalid(self, term):
        bad = ['', "None"]
        if term in bad or len(term) == 0:
            return False
        return True

    def preprocess_query(self, query):
        query = query.split(" ")
        for index, term in enumerate(query):
            if self.stem_on == True:
                query[index] = self.porter_stemming.stem(
                    term, 0, len(term)-1).lower().replace("\n", "")
            else:
                query[index] = term.lower().replace("\n", "")

        query = list(filter(self.remove_invalid, query))
        query_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
        for term in query:
            query_dict[self.char_to_index(term[0])].append(term)
        return query, query_dict

    def search_index(self, query):
        relevant_docs = {}
        relevant_postings = {}
        # Parse Query
        # Stem query if needed
        query, query_dict = self.preprocess_query(query)
        for range in query_dict.keys():
            if query_dict[range]:

                start_time = time.time()
                # load postings range
                self.load_postings_range(query_dict[range][0][0])
                # print("\nload time:", time.time() - start_time)

            for term in query_dict[range]:
                # print("term:", term)

                start_time = time.time()
                # Get doc frequency
                doc_freq = self.freqs.get(term, 0)
                # print("df time:", time.time() - start_time)

                start_time = time.time()
                # Get docs where query term is found. Returns an empty ditc if not
                relevant_postings[term] = self.postings.get(term, {})
                # print("look up time:", time.time() - start_time)

                start_time = time.time()
                relevant_docs = relevant_docs | relevant_postings[term].keys()
                # print("merge time:", time.time() - start_time)

                # print(doc_freq, len(relevant_postings[term]))

        start_time = time.time()
        bm25 = BestMatch25(query, relevant_docs,
                           relevant_postings, self.freqs, self.corpus_info, self.load_cd())
        # print("bm25 load time:", time.time() - start_time)

        start_time = time.time()
        scores = bm25.fit()
        # print("calc time:", time.time() - start_time)

        del bm25

        start_time = time.time()
        scores.sort(key=lambda scores: scores[1], reverse=True)
        # print("sort time:", time.time() - start_time)

        start_time = time.time()
        count = 0
        for doc_id, score in scores[:20]:
            count += 1
            print(
                f"Rank: {count}\nDoc ID: {doc_id}\nTitle: {self.titles[doc_id]}\nScore: {score}\n")
        # print("print time:", time.time() - start_time)

        # print(query, len(relevant_docs), len(relevant_postings), relevant_docs)
        self.postings = {}

    def strToBool(self, string):
        # Converts str to bool
        return string.lower() == "y"

    def search(self):
        self.stem_on = True
        self.stopwords_on = False
        self.load_df()
        self.load_dt()
        self.load_ci()

        # Get query term from user
        query = input("Enter a one word query: ")

        # Handle queries
        query_count = 0
        total_times = 0
        while query != "ZZEND":
            query_count += 1
            start_time = time.time()
            self.search_index(query)
            exec_time = time.time() - start_time
            total_times += exec_time
            print(f"The query took {exec_time} seconds.\n\n\n")
            query = input("Enter a one word query: ")

        print("\n=======================================")
        print("ENDING")
        print("=======================================")
        print(f"Average query time: {total_times/query_count}")
        print("=======================================")


Q = Query()
Q.search()