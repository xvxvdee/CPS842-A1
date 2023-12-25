from collections import OrderedDict
from bs4 import BeautifulSoup as bs

import numpy as np

import json
import gzip
import regex as re
import sys
import time

import porterAlgo  # Porter Stemming Algo


class int64_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


class index_construction:

    stop_words = []
    document_title_dict = {}
    document_frequency = {}
    postinglist_dict = {}
    clean_docs_dict = {}

    def __init__(
        self,
        file_path,
        stopwords_path,
        stem_on,
        stopwords_on,
        title_file_name="docTitleDict",
        posting_file_name="postingListDict",
        df_file_name="documentFrequency",
        clean_docs_file_name="cleanDocsDict"
    ):
        self.file_path = file_path
        self.stopwords_path = stopwords_path
        self.stem_on = stem_on
        self.stopwords_on = stopwords_on
        self.doctitle_file_name = title_file_name
        self.postings_file_name = posting_file_name
        self.df_file_name = df_file_name
        self.clean_docs_file_name = clean_docs_file_name

    def get_extension(self):
        # Get correct File Path Extension
        if self.stem_on:
            extension = "_stem"
        else:
            extension = "_nostem"
        if self.stopwords_on:
            extension += "_stop.json"
        else:
            extension += "_nostop.json"
        return extension

    def get_stopwords(self):
        if not self.stopwords_on:
            with open(self.stopwords_path, 'r') as stopword:
                self.stop_words = [word.replace("\n", "") for word in stopword]

    def porter_stemming(self, uncleaned_word):
        porterstemming_algo = porterAlgo.PorterStemmer()

        if uncleaned_word.isnumeric():
            return uncleaned_word  # keep numbers as is

        word = re.sub('[^a-zA-Z]', '', uncleaned_word)  # remove special chars

        if self.stem_on == True:
            word_cleaned = porterstemming_algo.stem(word, 0, len(
                word)-1).lower().replace("\n", "")  # lemmatize token
        else:
            word_cleaned = word.lower().replace("\n", "")

        # remove stopwords
        if word_cleaned not in self.stop_words and len(word_cleaned) > 2:
            return word_cleaned
        else:
            return 'None'

    def remove_none(self, word):
        bad = ['None']
        if word in bad:
            return False
        return True

    def doc_frequency(self, doc_set):
        for word in doc_set:
            self.document_frequency[word] = 1 + self.document_frequency.get(word, 0)

    def get_window(self, size, index, doc):
        if index < size:
            window = doc[:index + size + 1]
        else:
            window = doc[index-size:index + size + 1]
        return window

    def postings_list(self, doc_id, doc):
        for index, term in enumerate(doc):
            if term in self.postinglist_dict:
                if doc_id in self.postinglist_dict[term]:
                    self.postinglist_dict[term][doc_id][0] += 1
                    self.postinglist_dict[term][doc_id][1] += f',{index}'
                else:
                    self.postinglist_dict[term][doc_id] = [
                        1, f'{index}']
            else:
                self.postinglist_dict[term] = {
                    str(doc_id): [1, f'{index}']}

    def process_contents(self, line):
        data = json.loads(line)  # Load JSON
        doc_id = str(data['id'])
        title = data['title']
        self.document_title_dict[doc_id] = title

        # Deal with HTML content
        contents = bs(data['contents'], "html.parser")

        # remove html tags from content
        contents_stripped = " ".join(contents.stripped_strings)
        contents_stripped = contents_stripped.split(" ")

        porter_stem = list(
            map(self.porter_stemming, contents_stripped))  # stem content
        porter_stem = list(filter(self.remove_none, porter_stem))
        return [doc_id, porter_stem]

    def process_files(self):
        count = 0
        extension = self.get_extension()
        with gzip.open(self.file_path, 'rb') as file:
            for wiki in file:
                count += 1

                contents = self.process_contents(wiki)

                # Update Positing List
                self.postings_list(contents[0], contents[1])
                # Update Doc Frequency
                self.doc_frequency(set(contents[1]))

                # Save cleaned
                self.clean_docs_dict[contents[0]] = " ".join(contents[1])  # stringify to reduce space

                if count % 10 == 0:
                    # print(count, sys.getsizeof(self.postinglist_dict),
                    #       sys.getsizeof(self.clean_docs_dict))
                    print(count)
                if count % 100 == 0:
                    with open("lastupdate.txt", 'w') as f:
                        f.write(f'{count}{extension}')
                    self.save_jsonfile()

                if count == 30:
                    break
            with open("lastupdate.txt", 'w') as f:
                f.write(f'{count}{extension}')

    def load_jsonfile(self):
        extension = self.get_extension()
        with open(self.postings_file_name+extension, "r") as postings:
            self.postinglist_dict = json.load(postings)

        with open(self.df_file_name+extension, "r") as freqs:
            self.document_frequency = json.load(freqs)

        with open(self.doctitle_file_name+extension, "r") as titles:
            self.document_title_dict = json.load(titles)

        with open(self.clean_docs_file_name+extension, 'r') as clean:
            self.clean_docs_dict = json.load(clean)

    def save_jsonfile(self):
        self.postinglist_dict = OrderedDict(
            sorted(self.postinglist_dict.items()))  # sorting dictionary
        self.document_frequency = OrderedDict(
            sorted(self.document_frequency.items()))  # sorting dictionary
        # self.document_title_dict = OrderedDict(
        #     sorted(self.document_title_dict.items()))  # sorting dictionary

        extension = self.get_extension()
        with open(self.postings_file_name+extension, 'w') as f:
            json.dump(self.postinglist_dict, f, cls=int64_encoder)

        with open(self.df_file_name+extension, 'w') as f:
            json.dump(self.document_frequency, f)

        with open(self.doctitle_file_name+extension, 'w') as f:
            json.dump(self.document_title_dict, f)

        with open(self.clean_docs_file_name+extension, 'w') as f:
            json.dump(self.clean_docs_dict, f)


IC = index_construction("C:/Users/deand/OneDrive/Documents/CPS 842/A1/trec_corpus_5000.jsonl.gz", "cacm_stopwords.txt", False, True)
# IC = index_construction(
#     r"/Users/nojiro/Desktop/CPS842/trec_corpus_5000.jsonl.gz", "cacm_stopwords.txt", False, True)
# IC = index_construction(r"C:\Users\jkyle\Desktop\CPS842\trec_corpus_5000.jsonl.gz", "cacm_stopwords.txt", False, False)


IC.get_stopwords()
# IC.load_jsonfile()
IC.process_files()
# IC.save_jsonfile()

# start_time = time.time()
# IC.process_files()
# exec_time = time.time() - start_time
# print(exec_time)
# IC.save_jsonfile()