import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

def filter_pair(pair, src_max_len, tgt_max_len):
    """
    Returns true if a sentence pair meets the length requirements, false otherwise.

    Args:
        pair ((str, str)): (source, target) sentence pair
        src_max_len (int): maximum length cutoff for sentences in the source language
        tgt_max_len (int): maximum length cutoff for sentences in the target language
    Returns:
         bool: true if the pair is shorter than the length cutoffs, false otherwise
    """
    return len(pair[0]) <= src_max_len and len(pair[1]) <= tgt_max_len


def space_tokenize(text):
    """
    Tokenizes a piece of text by splitting it up based on single spaces (" ").

    Args:
     text (str): input text as a single string

    Returns:
         list(str): list of tokens obtained by splitting the text on single spaces
    """
    return text.split(" ")


def prepare_data(path, src_max_len, tgt_max_len, tokenize_func=space_tokenize):
    """
    Reads a tab-separated data file where each line contains a source sentence and a target sentence. Pairs containing
    a sentence that exceeds the maximum length allowed for its language are not added.

    Args:
        path (str): path to the data file
        src_max_len (int): maximum length cutoff for sentences in the source language
        tgt_max_len (int): maximum length cutoff for sentences in the target language
        tokenize_func (func): function for splitting words in a sentence (default is single-space-delimited)

    Returns:
        list((str, str)): list of (source, target) string pairs
    """

    logger.info("Reading Lines from {}".format(path))
    # Read the file and split into lines
    pairs = []
    with open(path) as fin:
        for line in tqdm(fin):
            try:
                src, dst = line.strip().split("\t")
                pair = map(tokenize_func, [src, dst])
                if filter_pair(pair, src_max_len, tgt_max_len):
                    pairs.append(pair)
            except:
                logger.error("Error when reading line: {0}".format(line))
                raise

    logger.info("Number of pairs: %s" % len(pairs))
    return pairs


def prepare_data_from_list(src_list, tgt_list, src_max_len, tgt_max_len, tokenize_func=space_tokenize):
    """
    Reads a tab-separated data file where each line contains a source sentence and a target sentence. Pairs containing
    a sentence that exceeds the maximum length allowed for its language are not added.

    Args:
        src_list (list): list of source sequences
        tgt_list (list): list of target sequences
        src_max_len (int): maximum length cutoff for sentences in the source language
        tgt_max_len (int): maximum length cutoff for sentences in the target language
        tokenize_func (func): function for splitting words in a sentence (default is single-space-delimited)

    Returns:
        list((str, str)): list of (source, target) string pairs
    """
    if not len(src_list) == len(tgt_list):
        raise ValueError('source sequence list and target sequence list has different number of entries.')

    logger.info("Preparing pairs...")

    # Read the file and split into lines
    pairs = []

    for index, _ in tqdm(enumerate(src_list)):
        pair = map(tokenize_func, [src_list[index], tgt_list[index]])
        if filter_pair(pair, src_max_len, tgt_max_len):
            pairs.append(pair)

    logger.info("Number of pairs: %s" % len(pairs))
    return pairs


def read_vocabulary(path, max_num_vocab=50000):
    """
    Helper function to read a vocabulary file.

    Args:
        path (str): filepath to raw vocabulary file
        max_num_vocab (int): maximum number of words to read from vocabulary file

    Returns:
        set: read words from vocabulary file
    """
    logger.info("Reading vocabulary from {}".format(path))
    # Read the file and create list of tokens in vocabulary
    vocab = set()
    with open(path) as fin:
        for line in fin:
            if len(vocab) >= max_num_vocab:
                break
            try:
                vocab.add(line.strip())
            except:
                logger.error("Error when reading line: {0}".format(line))
                raise

    logger.info("Size of Vocabulary: %s" % len(vocab))
    return vocab

