import numpy as np
import pandas as pd
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier

X_train_temp = [] 
Y_train_temp = []

categories_repeats=[]
numerical_categories={}

with open("train_topics_keywords.tsv", encoding='utf-8') as file: #load tsv
       
    # Passing the TSV file to reader() function with tab delimiter. This function will read data from file
    tsv_file = csv.reader(file, delimiter="\t")
    # printing data line by line
    for line in tsv_file:
        Y_train_temp.append(line[1]) # targets
        X_train_temp.append(line[2]) # words related to a target


for i in range(len(X_train_temp)):
    numerical_categories[i] = Y_train_temp[i] # Assigning category a number
Y_train_temp = list(numerical_categories.keys())

for x in range(len(X_train_temp)):
    l = len(X_train_temp[x].split(","))
    lst = l*(numerical_categories[x]+",")
    categories_repeats.append(lst[:len(lst)-1])

X_train = ",".join(X_train_temp).split(",")
Y_train = ",".join(categories_repeats).split(",")

data = {"X_train":X_train,
"Y_train":Y_train}

bow_vectorizer = CountVectorizer(stop_words="english")
bowVect = bow_vectorizer.fit(X_train)
bowTrain = bow_vectorizer.transform(X_train)
bow_vectorizer.get_feature_names_out()

knn = KNeighborsClassifier(n_neighbors=1)
# training our classifier ; train_data.target will be having numbers assigned for each category in train data
clf = knn.fit(bowTrain, Y_train)
res=clf.predict(bow_vectorizer.transform(["I like wii sports and cartoons"]))
res1=clf.predict(bow_vectorizer.transform(["I", "like", "wii", "sports","and","cartoons"]))

print(res,res1)