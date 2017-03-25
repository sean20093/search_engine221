from lxml import html, etree
from lxml.html.clean import Cleaner
import pymongo
import os
import nltk
from nltk import stem
from nltk.corpus import stopwords
from urlparse import urlparse, urljoin
import re
import math0.

# some parameters used in the subsequent functions
param = dict()
param["weight"] = [5, 2, 1]
param["tokenizer"] = nltk.RegexpTokenizer(r"\w+\0?")                   # case: word 123 word1233 word_123 word\0
# param["tokenizer"] = nltk.RegexpTokenizer(r"\(\d{3}\)\d{3}-\d{4}"       # case: (949)232-9600
#                                           r"|\w+-\w+"                   # case: 3-15
#                                           r"|\d+:\d+"                   # case: 8:30
#                                           r"|\w+@{1}[\w\.]+"            # case: abc@uci.edu abc@email.com
#                                           r"|\w+\0?")                   # case: word 123 word1233 word_123 word\0
param["stemmer"] = stem.snowball.EnglishStemmer(ignore_stopwords=False)
param["stopwords"] = set(stopwords.words("English"))
param["d"] = 0.85


def create_index(index_table, doc_table, doc_url, url_doc, doc_dir):
    """
    Create index for the corpus (all the documents)
    :param index_table: the collection (table) storing the index
    :param doc_table:
    :param doc_url: a dict mapping doc_id to url
    :param url_doc: a dict mapping url to doc_id
    :param doc_dir: the root directory of the documents
    """
    index_table.create_index([("term", pymongo.ASCENDING)], unique=True)
    doc_table.create_index([('doc_id', pymongo.ASCENDING)], unique=True)
    index = dict()
    doc_info = dict()

    # Index all the documents
    for i in range(75):
        for j in range(500):
            doc_id = "%d/%d" % (i, j)
            doc_path = os.path.join(doc_dir, str(i), str(j))
            if not os.path.exists(doc_path):
                break
            if len(doc_url[doc_id]) > 100 and re.match(r".+/(.+)(/.+)*/\1/", doc_url[doc_id]):
                continue
            doc = index_doc(index, doc_path, doc_id, doc_url, url_doc)
            if doc is not None:
                doc_info[doc_id] = doc
        print("Directory %d completed!" % i)
        if (i + 1) % 25 == 0 or i == 74:
            update_db(index, index_table)
            index = dict()
    page_rank(doc_info, param["d"])
    doc_table.insert_many([{"doc_id": doc_id, "length": item["length"], "pagerank": item["prPrev"]}
                           for doc_id, item in doc_info.iteritems()], ordered=False)


def page_rank(doc_info, d):
    """
    Compute the PageRank of every document
    :param doc_info: a dict mapping doc_id to a dict containing the length, PageRank and outlinks of the document
    :param d: the damper factor
    """
    num_doc = len(doc_info)
    for iteration in range(5):
        for doc_id, item in doc_info.iteritems():
            item["prCur"] += 1 - d
            nlinks = len(item["outlinks"])
            for out_id in item["outlinks"]:
                doc_info[out_id]["prCur"] += d * (item["prPrev"] if iteration != 0 else 1.0/num_doc) / nlinks

        for doc_id, item in doc_info.iteritems():
            item['prPrev'] = item['prCur']
            item['prCur'] = 0


def update_db(index, collection):
    """
    Merge the index with the index stored in the database.
    :param index: the index to be merged
    :param collection: the collection (table) storing the index
    """
    for term, postings in index.iteritems():
        collection.update_one(
            {"term": term},
            {
                "$push": {"postings": {"$each": postings}},
            },
            upsert=True
        )


def index_doc(index, doc_path, doc_id, doc_url, url_doc):
    """
    Index a document and update the current index accordingly.

    Structure of index (dict):
    key: term  value: list of document items


    Structure of document item (list):
    [document_id, term_frequency, hit_list]

    Structure of hit (tuple):
    (type, position, isLastTerm)

    :param index: the index to be updated (type: dict)
    :param doc_path: path of the document (type: str)
    :param doc_id: id of the document (type: str)
    :param doc_url: a dict mapping doc_id to url (type: dict)
    :param url_doc: a dict mapping url to doc_id (type: dict)
    :return: a dict containing the length and outlinks of the document or None for invalid document (type: dict or None)
    """
    try:
        root = html.parse(doc_path).getroot()
        if root is None or root.find("head") is None:   # the document is not a web page
            return None
        outlinks = []
        # remove javascript, style, comments and other useless parts from html
        cleaner = Cleaner(style=True, links=False, meta=False, page_structure=False, frames=False, forms=False,
                          annoying_tags=False, safe_attrs_only=False)
        cleaner(root)
        text = [""]*3
        # title text
        title = root.find("head").find("title")
        if title is not None:
            text[0] = title.text_content()
        # header text
        for elem in root.iter("h1", "h2", "a"):
            if elem.tag == "a":
                url = urljoin(doc_url[doc_id], elem.get("href"))
                parsed = urlparse(url)
                if parsed.scheme:
                    url = url[len(parsed.scheme)+3:]
                if url in url_doc:
                    outlinks.append(url_doc[url])
            else:
                text[1] += elem.text_content()
                text[1] += "\0"
                elem.drop_tree()
        # other text
        body = root.find("body")
        if body is not None:
            text[2] = body.text_content()
        term_set = set()        # all the terms occurring in this document
        for i in range(len(text)):
            term_list = tokenize_stem(text[i])
            for pos, term in enumerate(term_list):
                is_end = False
                if i == 1 and term[-1] == "\0":
                    term = term[0:-1]
                    is_end = True
                term_set.add(term)
                if term not in index:
                    index[term] = [{"doc_id": doc_id, "nhits": 0, "tf": 0.0, "hits": list()}]
                elif index[term][-1]["doc_id"] != doc_id:
                    index[term].append({"doc_id": doc_id, "nhits": 0, "tf": 0.0, "hits": list()})   # add a new posting
                index[term][-1]["nhits"] += param["weight"][i]        # increase term frequency
                index[term][-1]["hits"].append((i, pos, is_end))       # add new hit to the hit list
        length = 0.0    # length of this document vector (tf-weighting as the dimensions of the document space)
        for term in term_set:
            tf = 1 + math.log(index[term][-1]["nhits"])
            index[term][-1]["tf"] = tf
            length += tf * tf
        return {"prPrev": 1, "prCur": 0, "outlinks": outlinks, "length": math.sqrt(length)}
    except etree.ParseError:
        print("Parse error!")
        return None


def tokenize_stem(text):
    """
    Tokenize a string and stem each terms
    :param text: the original string to be processed
    :return: a list of stemmed terms
    """
    term_list = param["tokenizer"].tokenize(text)
    final_list = list()
    for term in term_list:
        if term in param["stopwords"]:
            continue
        try:
            if term[-1] == "\0":
                final_list.append(param["stemmer"].stem(term[0:-1]) + "\0")
            else:
                final_list.append(param["stemmer"].stem(term))
        except IndexError:
            print(term)
    return final_list
