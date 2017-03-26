from googleapiclient.discovery import build
import pprint
#API_KEY="AIzaSyBaEI0o8NdDcq1lsoaAvly-ptTo2VnyLRY"
API_KEY="AIzaSyBCbgJNFAaqovLpnGNRX-EhJ-5ksbGD6x4"
#CX = "000871406312733320210:n0ht0gelmoc"
CX = "015572863640410483657:-6tknitvjsw"
#CX ="015572863640410483657:ecin8ok8a3k"

search_word = ["mondego", "machine learning", "software engineering", "security", "student affairs",
               "graduate courses", "Crista Lopes", "REST", "computer games", "information retrieval"]


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

#
# for keyword in search_word:
#     results = google_search(keyword+"site:ics.uci.edu", API_KEY, CX, num=5)
#     for result in results:
#         url = result['formattedUrl']
#         print url
#     pass

results = google_search("mondego "+"site:ics.uci.edu", API_KEY, CX, num=10)
print len(results)
for result in results:
    url = result['formattedUrl']
    print url


'''
results = google_search(
    'machine learning site:ics.uci.edu', API_KEY, CX, num=10)
length=len(results)
print length
for result in results:
    url= result['formattedUrl']
    print url
'''