import os
import pandas as pd
import string
import nltk


def count_tokens(text_input: str | list,
                 stop_words=[],
                 from_tokens=False,
                 ignore_uppercase=True,
                 ignore_punctuation=True,
                 ignore_nonalpha=True) -> dict:
    """
    gets a list of words (tokens) from a given text using the word-tokenizer
    from NLTK and counts the frequency of each word (types)
    :param text_input: a text as string or a pre-tokenized
    text as list of strings
    :param stop_words: a list of stop words
    to be excluded from the analysis
    :param from_tokens: option to pass list of tokens instead of a full text
    :param ignore_uppercase: should lower- and uppercase words be treated as one type?
    :param ignore_punctuation: should punctuation marks be counted?
    :param ignore_nonalpha: should numbers etc. be ignored in the count?
    :return: a dictionary {key = word, value = word frequency}
    """
    word_counts = {}
    if from_tokens:
        tokens = text_input
    else:
        # tokenize text:
        tokens = nltk.word_tokenize(text_input, language='german')
    if ignore_uppercase:
        # set all tokens to lowercase:
        tokens = [t.lower() for t in tokens]
    if ignore_punctuation:
        # remove punctuation:
        tokens = [t for t in tokens if t not in string.punctuation]
    if ignore_nonalpha:
        # contract hyphenated expressions (would be ignored otherwise):
        tokens = [t.replace('-', '') for t in tokens]
        # remove non-alphabetical characters:
        tokens = [t for t in tokens if t.isalpha()]
    if len(stop_words) >= 1:
        # remove stopwords:
        tokens = [t for t in tokens if t not in stop_words]
    # count tokens:
    for token in tokens:
        if token not in word_counts.keys():
            word_counts[token] = 1
        else:
            word_counts[token] += 1
    return word_counts


def get_frequency_df(text_input: str | list,
                     col_1='word',
                     col_2='frequency',
                     stop_words=[],
                     from_tokens=False,
                     ignore_uppercase=True,
                     ignore_punctuation=True,
                     ignore_nonalpha=True) -> pd.DataFrame:
    """
    gets a text and returns a data frame with word frequencies
    :param text_input: a text as string or a list of tokens
    :return: a pandas data frame
    """
    word_counts_dict = count_tokens(text_input=text_input,
                                    stop_words=stop_words,
                                    from_tokens=from_tokens,
                                    ignore_punctuation=ignore_punctuation,
                                    ignore_uppercase=ignore_uppercase,
                                    ignore_nonalpha=ignore_nonalpha)
    frequency_dict = {col_1: list(word_counts_dict.keys()),
                      col_2: list(word_counts_dict.values())}
    frequency_df = pd.DataFrame(frequency_dict)
    return frequency_df


def get_frequency_tables(text_collection: list[str | list],
                         doc_names: list[str],
                         stop_words=[],
                         save_csv=False,
                         target_dir=None,
                         to_dict=False,
                         t_index=False,
                         t_encoding='utf-8',
                         from_tokens=False,
                         ignore_uppercase=True,
                         ignore_punctuation=True,
                         ignore_nonalpha=True
                         ) -> dict | None | pd.DataFrame:
    """
    counts the absolute frequencies of words per text in a text collection
    and returns them as tabular data
    :param text_collection: list of texts or list of tokens
    :param doc_names: identifiers of the texts
    :param target_dir: the directory to save the csv-tables
    :param stop_words: list of stop words that should not be
    considered in the analysis
    :param save_csv: results are saved as csv-files
    :param to_dict: returns a dictionary, keys = text-identifiers, values = frequency tables
    :return: None | dict | the combined results in a merged data frame
    """
    try:
        if len(text_collection) != len(doc_names):
            raise IndexError('One document name must be given '
                             'for each text in the collection.')
        if save_csv:
            if not target_dir:
                raise OSError('A valid path to an existing directory '
                              'must be given to save your results.')
            for count, text in enumerate(text_collection):
                df = get_frequency_df(text_input=text,
                                      stop_words=stop_words,
                                      from_tokens=from_tokens,
                                      ignore_punctuation=ignore_punctuation,
                                      ignore_uppercase=ignore_uppercase,
                                      ignore_nonalpha=ignore_nonalpha
                                      )
                file_path = os.path.join(target_dir,
                                         str(doc_names[count]) + '_frequencies.csv')
                df.to_csv(file_path, index=t_index, encoding=t_encoding)
            print('Data saved in: ' + target_dir)
            return None
        elif to_dict:
            df_dict = {}
            for count, text in enumerate(text_collection):
                df = get_frequency_df(text_input=text,
                                      stop_words=stop_words,
                                      from_tokens=from_tokens,
                                      ignore_punctuation=ignore_punctuation,
                                      ignore_uppercase=ignore_uppercase,
                                      ignore_nonalpha=ignore_nonalpha
                                      )
                df_dict[doc_names[count]] = df
            return df_dict
        else:
            data_table = pd.DataFrame(columns=['word'])
            for count, text in enumerate(text_collection):
                df = get_frequency_df(text_input=text,
                                      col_2=doc_names[count],
                                      stop_words=stop_words,
                                      from_tokens=from_tokens,
                                      ignore_punctuation=ignore_punctuation,
                                      ignore_uppercase=ignore_uppercase,
                                      ignore_nonalpha=ignore_nonalpha
                                      )
                data_table = data_table.merge(df, how='outer')
            return data_table
    except Exception as e:
        print('An error occurred:\n', e)
    return None
