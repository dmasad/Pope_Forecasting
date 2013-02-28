from __future__ import division
from collections import defaultdict

def clean_word(word, punctuation):
    """
    Cleans all the punctuation marks from a word.

    Args:
        word: target word
        punctuation: string of punctuation tokens.
    Returns:
        The word cleaned of punctuation marks at the beginning and end, and
        converted to lower-case.
    """
    try: 
        while len(word)>0:
            while word[0] in punctuation:
                word = word[1:]
            while word[-1] in punctuation:
                word = word[:-1]
            break
        return word.lower()
    
    except:
        return ""


def find_ngrams(text, n=1, punctuation=""","';:-?!.""", stop_words=[]):
    """
    Sparse-vectorizer: cleans the text and returns a dictionary of n-gram counts

    Args:
        text: the input text; assumed to be a sentence.
        n: the number of tokens per n-gram. Defaults to 1.
        punctuation: String of punctuation tokens to ignore.
        stop_words: a list of n-grams to ignore; empty by default.
    
    Returns:
        A term vector, of the form
            {term: count, term: count...}
    """
    ngrams = defaultdict(int)

    # Clean the word list
    words = [clean_word(word, punctuation) for word in text.split()] 
    words = [word for word in words if len(word)>0] #Remove nulls.
    while n > 0:
        # Repeat for all values >= n:        
        for i in range(len(words)-n+1):
            new_ngram = []
            counter = 0
            while len(new_ngram)<n:
                new_ngram.append(words[i+counter])
                counter += 1
            new_ngram = tuple(new_ngram)
            if new_ngram not in stop_words:
                ngrams[new_ngram] += 1
        n -= 1
    
    return ngrams

def jaccard_similarity(vector1, vector2):
    '''
    Compute Jaccard Similarity between two sparse vectors,
    represented as dicts.
    '''

    all_keys = set(vector1.keys() + vector2.keys())
    union = len(all_keys)
    intersection = 0
    for key in all_keys:
        if key in vector1 and key in vector2:
            intersection += 1
    return intersection / union


def create_distance_matrix(sparse_vectors, metric, inverse=False):
    '''
    Inputs are sparse vectors and a metric function; 
    pre-computes all the distances and returns a function 
    for accessing them. 

    Args:
        sparse_vectors: dictionary of {'name': {sparse: vectors},...}
        metric: distance metric function
        inverse: bool on whether to invert the metric

    Returns:
        A closure-defined function wrapped around a pre-computed Similarity
        matrix.

    '''
    distances = {}
    for doc1, vector1 in sparse_vectors.items():
        distances[doc1] = {}
        for doc2, vector2 in sparse_vectors.items():
            if doc1 != doc2 and doc2 not in distances:
                distances[doc1][doc2] = metric(vector1, vector2)
                if inverse: 
                    distances[doc1][doc2] = 1 - distances[doc1][doc2]

    def find_distance(doc1, doc2):
        '''
        Find the distance between doc1 and doc2
        '''
        if doc2 not in distances[doc1]:
            doc1, doc2 = doc2, doc1
        return distances[doc1][doc2]
    return find_distance





