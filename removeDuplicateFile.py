import os, sys, md5
from lxml import html, etree


def remove_duplicate():
    md5_dict = dict()
    for i in range(75):
        for j in range(500):
            doc_id = "%d\\%d" % (i, j)
            doc_path = "D:\UCI\cs 221 information\project 3\WEBPAGES_RAW\\" + doc_id
            if not os.path.exists(doc_path):
                break
            md5_calculate(doc_path, doc_id, md5_dict)


def md5_calculate(doc_path, doc_id, md5_dict):
    root = html.parse(doc_path).getroot()
    if root is None:
        return False
    if root.find("head") is None:  # the document is not a web page
        print("head missing: " + doc_id)
        return False
    with open(doc_path, "r") as f:
        md5_value = md5.new(f.read()).digest()
    if md5_value in md5_dict:
        print doc_id + "indentical with" + md5_dict.get(md5_value)
    else:
        md5_dict.setdefault(md5_value, doc_id)

    pass

#remove_duplicate()


f1 = open("D:\UCI\cs 221 information\project 3\WEBPAGES_RAW\\2\\22", "r")
f2 = open("D:\UCI\cs 221 information\project 3\WEBPAGES_RAW\\0\\257", "r")
print md5.new(f1.read()).digest()
print md5.new(f2.read()).digest()


''''
hello = dict()
value = md5.new(f1.read()).digest()
hello.setdefault(value, "0\\2")
md5_value = md5.new(f2.read()).digest()
if md5_value in hello:
    print "0//2" + "indentical with" + hello.get(md5_value)
else:
    hello.setdefault(md5_value, "90")
    print "add"
'''