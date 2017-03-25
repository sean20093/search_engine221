import math
from DoughMaking import tokenize_stem


def search(query, index_table, doc_info, ranker):
    num_doc = len(doc_info)
    term_list = tokenize_stem(query)
    query_vec = dict()
    for term in term_list:
        if term not in query_vec:
            query_vec[term] = 1
        else:
            query_vec[term] += 1
    scores = dict()
    for term, freq in query_vec.iteritems():
        tf_query = 1 + math.log(freq)
        item = index_table.find_one({"term": term})
        if item is None:
            continue
        posting_list = item["postings"]                         # documents where the term occurs
        idf = math.log(float(num_doc) / len(posting_list))      # inverse document frequency
        for posting in posting_list:
            doc_id = posting["doc_id"]
            tf_doc = posting["tf"]                              # term frequency weighting
            # tf_doc = 1 + math.log(posting["nhits"])
            if doc_id not in scores:
                scores[doc_id] = tf_doc * tf_query * idf
            else:
                scores[doc_id] += tf_doc * tf_query * idf
    if ranker == 1:
        for doc_id in scores.keys():
            # scores[doc_id] /= max(doc_info[doc_id]["length"], 10)
            # scores[doc_id] /= max(math.log(doc_info[doc_id]["length"]), 1)
            scores[doc_id] /= doc_info[doc_id]["length"]
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[0:min(100, len(scores))]
    for i in range(len(sorted_scores)):
        doc_id = sorted_scores[i][0]
        score = 0.4*sorted_scores[i][1] + 0.6*doc_info[doc_id]["pagerank"]
        sorted_scores[i] = (doc_id, score)

    return sorted(sorted_scores, key=lambda x: x[1], reverse=True)
