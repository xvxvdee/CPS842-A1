This assignment was done in a group of 2.

# Inverted Index and Query

This is a python program that builds an inverted index from a collection of Wikipedia articles and performs single term queries. The program can handle different options for stemming and stop word removal.

## Dataset

The dataset consists of more than 200,000 English Wikipedia pages submitted for TREC fair ranking. Every page includes an ID, the article's title, the page's URL, and the HTML for its content, all in a JSON file compressed with gzip. A subset of 50,000 documents are used for this assignment's dataset due to RAM restrictions.

## Dependencies

- Python 3.8 or higher
- BeautifulSoup from bs4
- gzip
- regex

## Usage

### Indexing

To create the index, run the `indexConstruction.py` file with the following arguments:

- `file_path`: the path to the gzip dataset file
- `stopwords_path`: the path to the cacm_stopwords text file
- `stem_on`: a boolean value indicating whether to apply stemming or not
- `stopwords_on`: a boolean value indicating whether to remove stop words or not

For example:

```python
python indexConstruction.py "path/to/zipped/data" "cacm_stopwords.txt" True True
```

This will create the index with stemming and stop word removal enabled, and save it as JSON files in the same directory.

### Querying

To query the index, run the `query.py` file with no arguments. This will prompt the user to choose whether to query with stemming or stop word removal enabled. Type `y` for yes and `n` for no. Once selected, the corresponding index files will be loaded and the user will be asked to enter a word to be queried. The program will display the document frequency and the top 20 documents that contain the word, along with the term frequency and the positions. The program will also show the time it took to process the query. To exit the program, type `ZZEND`.

For example:

```python
python query.py
Do you want to query with stemming? (y/n) y
Do you want to query with stopwords? (y/n) n
Enter a word to be queried: algorithm
Document Frequency:  104
Doc ID:  5a0c1c9e55b14b36ce7b2c6f
Title:  Algorithm
Term Frequency:  38
Positions:  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
...
Query time:  0.001 seconds
Enter a word to be queried: ZZEND
```
