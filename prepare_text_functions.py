import os
import re


def prepare_text(source_path: str,
                 file_encoding='utf-8',
                 target_path='',
                 save_txt=False) -> str | None:
    error_message = (f'{source_path} cannot be decoded, '
                     f'check file type/encoding: \n\t')
    # special characters from 'fraktur'-print to be replaced for normalizing the text:
    translation = {'/': '',
                   'ꝛ': 'r',
                   'ſ': 's',
                   'aͤ': 'ä',
                   'oͤ': 'ö',
                   'uͤ': 'ü',
                   'ñ': 'n',
                   'ÿ': 'y'
                   }
    # pattern for character replacements:
    re_char = re.compile('|'.join(map(re.escape, translation)))
    # pattern to find any string inbetween angular brackets, including the brackets:
    re_annotations = re.compile('\\[.*?]')
    with open(source_path, 'r', encoding=file_encoding) as txt_file:
        try:
            text_content = txt_file.read()
        except (UnicodeError, UnicodeDecodeError) as error:
            print(error_message, error)
            text_content = None
    if text_content:
        # remove chapter / page numbers / annotations
        text_cleaned = re.sub(re_annotations, '', text_content)
        # remove whitespace characters
        text_cleaned = re.sub('\x0c', '', text_cleaned)
        # join separated words at line breaks:
        text_cleaned = text_cleaned.replace('-\n', '')
        # replace newline with whitespace
        text_cleaned = re.sub('\n', ' ', text_cleaned)
        # replace special characters from 'fraktur':
        text_cleaned = re_char.sub(lambda match: translation[match.group(0)],
                                   text_cleaned)
        if save_txt:
            with open(target_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text_cleaned)
            print(f'Cleaned text saved under: {target_path}')
        else:
            return text_cleaned
    else:
        return None


def prepare_text_collection(source_dir: str,
                            corpus_encoding='utf-8',
                            target_path='',
                            save_txt=False) -> str | None:
    collection_cleaned = []
    for filename in sorted(os.listdir(source_dir)):
        file_path = os.path.join(source_dir, filename)
        if (os.path.isfile(file_path)
                and filename.endswith('.txt')):
            text_cleaned = prepare_text(file_path, file_encoding=corpus_encoding)
            collection_cleaned.append(text_cleaned)
    try:
        text_joined = '\n'.join(collection_cleaned)
    except TypeError as te:
        print(te)
        text_joined = None
    if text_joined:
        if save_txt:
            with open(target_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text_joined)
            print(f'Cleaned and joined text saved under: {target_path}')
        else:
            return text_joined
    else:
        return None
