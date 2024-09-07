from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os


def get_tf_idf_tables(text_collection: list[str],
                      doc_names: list[str],
                      stop_words=None,
                      save_csv=False,
                      target_dir=None,
                      to_dict=False,
                      t_index=False,
                      t_encoding='utf-8'
                      ) -> pd.DataFrame | dict | None:
    """
    Calculates the tf-idf score for each word in a text corpus
    using the TfidfVectorizer from scikit learn package.
    Returns a table for each text in the collection
    :param text_collection: a list of strings
    :param doc_names: list of names of the documents to be analyzed
    :param stop_words: list of stop words (default = None)
    :param save_csv: saves a table for each text as csv-file
    :param target_dir: the directory where the csv-files are to be stored
    :param to_dict: returns the tables in a dictionary
    (keys = document names, values = data frames)
    :return: None | dict | the combined results in a merged data frame
    """
    try:
        if len(text_collection) != len(doc_names):
            raise IndexError('One document name must be given '
                             'for each text in the collection.')
        vectorizer = TfidfVectorizer(max_df=0.7, min_df=1, stop_words=stop_words,
                                     use_idf=True, norm=None, strip_accents='unicode')
        transformed_documents = vectorizer.fit_transform(text_collection)
        transformed_documents_as_array = transformed_documents.toarray()
        if save_csv:
            if not target_dir:
                raise OSError('A valid path to an existing directory '
                              'must be given to save your results.')
            for count, doc in enumerate(transformed_documents_as_array):
                tf_idf_tuples = list(zip(vectorizer.get_feature_names_out(), doc))
                one_doc_as_df = (pd.DataFrame.from_records(tf_idf_tuples,
                                                           columns=['word', 'tf_idf_score']))
                file_path = os.path.join(target_dir, str(doc_names[count]) + '_tf-idf.csv')
                one_doc_as_df.to_csv(file_path, index=t_index, encoding=t_encoding)
            print('Data saved in: ' + target_dir)
            return None
        elif to_dict:
            df_dict = {}
            for count, doc in enumerate(transformed_documents_as_array):
                tf_idf_tuples = list(zip(vectorizer.get_feature_names_out(), doc))
                one_doc_as_df = (pd.DataFrame.from_records(tf_idf_tuples,
                                                           columns=['word', 'tf_idf_score']))
                df_dict[doc_names[count]] = one_doc_as_df
            return df_dict
        else:
            data_table = pd.DataFrame(columns=['word'])
            for count, doc in enumerate(transformed_documents_as_array):
                tf_idf_tuples = list(zip(vectorizer.get_feature_names_out(), doc))
                one_doc_as_df = (pd.DataFrame.from_records(tf_idf_tuples,
                                                           columns=['word', doc_names[count]]))
                data_table = data_table.merge(one_doc_as_df, how='outer')
            return data_table
    except Exception as e:
        print('An error occurred:\n', e)
    return None
