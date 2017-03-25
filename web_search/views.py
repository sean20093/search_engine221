# Create your views here.

from django.shortcuts import render
from DoughMaking import create_index
from search import search
import pymongo
import os
import json
import math
from urlparse import urlparse
from googleapiclient.discovery import build

API_KEY="AIzaSyAJ7TmFWKCWhM3pMt_hKy-y1Z4BltzIn8w"
CX = "016831962112297716882:drpelfwvm7e"

DOC_DIR = "webpages"
client = pymongo.MongoClient('localhost', 27017)
db = client.noodledb
collections = db.collection_names()
index_table = db.index_snowball
doc_table = db.doc_info
with open(os.path.join(DOC_DIR, "bookkeeping.json"), "r") as f:
    doc_url = json.load(f)
with open(os.path.join(DOC_DIR, "url_doc.json"), "r") as f:
    url_doc = json.load(f)
if "index_snowball" not in collections:
    create_index(index_table, doc_table, doc_url, url_doc, DOC_DIR)
doc_info = {item["doc_id"]: {"length": item["length"], "pagerank": item["pagerank"]} for item in doc_table.find()}
# with open(os.path.join(DOC_DIR, "doc_info.json"), "w") as f:
#     json.dump(doc_info, f)


def search_page(request):
    if "query" not in request.GET:
        return render(request, "web_search/index.html")
    else:
        query = request.GET["query"]
        ranker = int(request.GET["r"]) if "r" in request.GET else 1
        results_all = search(query, index_table, doc_info, ranker)
        results = results_all[0:20]
        for i in range(len(results)):
            r = results[i]
            url = "http://" + doc_url[r[0]]
            results[i] = (url, r[0]+": "+url, r[1])     # url, anchor, score
        # Compute the NDCG
        service = build("customsearch", "v1", developerKey=API_KEY)
        res = service.cse().list(q=query+" site:ics.uci.edu", cx=CX, num=10).execute()
        urls = [result['formattedUrl'] for result in res['items']]
        valid_urls = dict()
        i = 0
        for url in urls:
            print url
            if i > 4:
                break
            parsed = urlparse(url)
            if parsed.scheme:
                url = url[len(parsed.scheme)+3:]
            if url[-1] == "/":
                url = url[0:-1]
            if url in url_doc:
                valid_urls[url] = i
                i += 1
        print valid_urls
        dcg = 0
        for i in range(5):
            url = results[i][0][7:]
            if url in valid_urls:
                dcg += (5-valid_urls[url]) / (math.log(i+1, 2) if i > 0 else 1)
        ndcg = dcg / (5 + 4 + 3/math.log(3, 2) + 2/math.log(4, 2) + 1/math.log(5, 2))
        print ndcg
        return render(request, "web_search/results.html", {"results": results})

