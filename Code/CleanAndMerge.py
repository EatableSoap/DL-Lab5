import json
import os
import re


def clean(jsonDict):
    title = jsonDict['title']
    url = jsonDict['url']
    content = jsonDict['content']
    pattern = re.compile(r'<.*?>')
    title = re.sub(pattern, '', title)
    content = re.sub(pattern, '', content)
    cleanedJson = {'title': title, 'content': content}
    return {url: json.dumps(cleanedJson,indent=2,ensure_ascii=False)}


def merge(mergePath,resultPath):
    newsDict = {}
    for root,dirs,files in os.walk(mergePath):
        for file in files:
            with open(os.path.join(root,file),'r',encoding='utf-8') as f:
                datas = json.load(f)
                for data in datas:
                    cleanData = clean(data)
                    newsDict.update(cleanData)
    for idx,kv in enumerate(newsDict.items()):
        with open(os.path.join(resultPath,'新闻_'+str(idx+1)+'.txt'),'w',encoding='utf-8') as f:
            f.write(kv[1])
    return


if __name__ == '__main__':
    toBeMergedPath = r'..\CrawlerResult'
    toBeRestoredPath = r'..\Data\新闻'
    merge(toBeMergedPath,toBeRestoredPath)
