import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import json

# load Hainhofer corpus:
w_dir = os.getcwd()
source_hainhofer = os.path.join(w_dir, 'korpus_hainhofer.csv')
# transfer to data frame:
df_h = pd.read_csv(source_hainhofer)
# get list of texts:
text_h = df_h.text.to_list()

# get all terms of corpus with max_df=1.0 (default setting)
vectorizer = CountVectorizer()
transformed_documents = vectorizer.fit_transform(text_h)
terms_all = set(vectorizer.get_feature_names_out())

# get subset of terms:
# -> terms with document frequency higher than the given threshold are ignored
vectorizer = CountVectorizer(max_df=0.95, min_df=1)
transformed_documents_weighted_l = vectorizer.fit_transform(text_h)
terms_weighted_l = set(vectorizer.get_feature_names_out())

vectorizer = CountVectorizer(max_df=0.9, min_df=1)
transformed_documents_weighted_s = vectorizer.fit_transform(text_h)
terms_weighted_s = set(vectorizer.get_feature_names_out())

# cast difference of the two sets two list:
stop_words_hainhofer_small = sorted(list(terms_all - terms_weighted_l))
stop_words_hainhofer_large = sorted(list(terms_all - terms_weighted_s))

# save stop words list as json file (can be loaded directly as a python list):
path_small = os.path.join(w_dir, 'stopwords_hainhofer_small.json')
with open(path_small, 'w') as outfile:
    outfile.write(json.dumps(stop_words_hainhofer_small))

path_large = os.path.join(w_dir, 'stopwords_hainhofer_large.json')
with open(path_large, 'w') as outfile:
    outfile.write(json.dumps(stop_words_hainhofer_large))
