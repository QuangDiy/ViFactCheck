from BM25 import BM25Okapi
import nltk

def similarities(context, query):
    sentences = nltk.sent_tokenize(context)
    tokenized_sentences = [str(doc).split(" ") for doc in sentences]
    bm25 = BM25Okapi(tokenized_sentences)
    tokenized_query = query.split(" ")

    # doc_scores = bm25.get_scores(tokenized_query)
    bm25_output = bm25.get_top_n(tokenized_query, sentences, n = 3)
    
    return bm25_output