import os
import pandas as pd


def get_text_content(f_path: str, f_encoding='utf-8') -> str:
    """
    gets the content of a text file and returns it as string
    if text cannot be decoded, an error message is printed, None returned
    :param f_path: path to the text file
    :param f_encoding: encoding of the text source, default='utf-8'
    :return: text content of the file as string
    """
    error_message = (f'{f_path} cannot be decoded, '
                     f'check file type/encoding: \n\t')
    with open(f_path, 'r', encoding=f_encoding) as file:
        try:
            text_content = file.read()
        except (UnicodeError, UnicodeDecodeError) as error:
            print(error_message, error)
            text_content = None
        return text_content


def get_text_corpus(corpus_path: str, corpus_encoding='utf-8') -> tuple:
    """
    gets the text content of a corpus as strings
    :param corpus_path: path to the directory with the text files
    :param corpus_encoding: encoding of the corpus, default='utf-8'
    :return: the plain text of the corpus as a list of strings,
    identifiers of the texts in the corpus retrieved from the filenames
    """
    text_content = []
    text_ids = []
    for filename in sorted(os.listdir(corpus_path)):
        file_path = os.path.join(corpus_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            file_name, file_extension = os.path.splitext(filename)
            text_id = file_name.lower().replace(' ', '_')
            file_content = get_text_content(file_path, corpus_encoding)
            if file_content:
                text_content.append(file_content)
                text_ids.append(text_id)
    return text_content, text_ids


def to_csv(corpus_dict: dict, target_path: str, csv_encoding='utf-8') -> None:
    """
    creates a data frame from a given dictionary,
    the data is then saved as csv file
    :param corpus_dict: dictionary with the text content of and additional
     information on the files in the corpus under examination
    :param target_path: path where the csv file is to be saved
    :param csv_encoding: encoding of the target file, default='utf-8'
    :return: None
    """
    try:
        corpus_df = pd.DataFrame(corpus_dict)
        corpus_df.to_csv(target_path, index=False, encoding=csv_encoding)
        print(f'Dataset saved under: {target_path}')
    except ValueError as ve:
        print(f'Unable to create csv-file from given data: \n\t{ve}')
