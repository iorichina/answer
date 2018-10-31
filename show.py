import sys
import random
import argparse
import time
import json
import requests
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

db = {"answers": [], "saved_topics": {}}
answer_ids = []
maxnum = 100


def set_maxnum(maxnum1):
    global maxnum
    maxnum = maxnum1


def get_answers(topic_id):
    global db
    page_no = 0
    while True:
        is_saved = topic_id in db['saved_topics']
        is_saved = is_saved and page_no in db['saved_topics'][str(topic_id)]
        if is_saved:
            page_no += 1
            continue
        # print(topic_id, page_no)
        print('.', end='')
        sys.stdout.flush()
        is_end = get_answers_by_page(topic_id, page_no)
        page_no += 1
        if is_end:
            break


def get_answers_by_page(topic_id, page_no):
    global db, answer_ids, maxnum
    limit = 10
    offset = page_no * limit
    url = "https://www.zhihu.com/api/v4/topics/" + str(topic_id) + "/feeds/essence?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.annotation_detail%2Ccontent%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.annotation_detail%2Ccontent%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.annotation_detail%2Ccomment_count&limit="+str(limit)+"&offset=" + str(offset)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }
    try:
        r = requests.get(url, verify=False, headers=headers)
    except requests.exceptions.ConnectionError:
        return False
    content = r.content.decode("utf-8")
    data = json.loads(content)
    is_end = data["paging"]["is_end"]
    items = data["data"]
    if len(items) <= 0:
        return True

    for item in items:
        if maxnum <= 0:
            return True
        answer_id = item["target"]["id"]
        if answer_id in answer_ids:
            continue
        if item['target']['type'] != "answer":
            continue
        if int(item["target"]["voteup_count"]) < 1000:
            continue
        if len(item['target']['content']) > 50:
            continue
        answer_ids.append(answer_id)
        # answer = {'target': {
        #     'question': {'title': item["target"]["question"]["title"]},
        #     'content': item["target"]["content"]
        # }}
        # db['answers'].append(answer)
        # db['saved_topics'][str(topic_id)] = page_no

        question = item["target"]["question"]["title"]
        answer = item["target"]["content"]
        if answer.find('<') > -1 and answer.find('>') > -1:
            pass
            # answer = BeautifulSoup(answer, 'html.parser').string
        print("\nQ: {}\nA: {}".format(question, answer))
        maxnum -= 1
    return is_end


def query():
    items = db['answers']
    for item in items:
        question = item["target"]["question"]["title"]
        answer = item["target"]["content"]
        print("\nQ: {}\nA: {}".format(question, answer))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", help="max data",
                        action="store_true", dest="max", default=100)
    args = parser.parse_args()
    set_maxnum(args.max)

    topic_ids = [19554298, 19552330, 19565652, 19580349, 19939299,
                 19555547, 19594551, 19552832, 19577377, 19552826, 19615452]
    # print(topic_ids)
    topic_ids.sort(key=lambda x: random.randint(-1, 1))
    # print(topic_ids)
    for topic_id in topic_ids:
        pass
        get_answers(topic_id)
    # query()
