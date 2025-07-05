import json
from openai import OpenAI


def singleRound(client, prompt, testText, extractResult=None):
    # return optimized prompt
    if extractResult is None:
        messages = [{"role": "user", "content": prompt.replace("[待插入新闻文本]", testText)}]
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages
        )
        extractResult = response.choices[0].message.content

    evalPrompt = (
        f'你目前从事提示词优化方面的工作，并且你是这个领域的专家。\n你的任务是：首先仔细阅读给出的测试文本、原始提示词和输出结果，然后根据你的经验，'
        f'评估通过这个提示词对测试文本进行的操作的效果，最后给出能更好完成提示词对应任务的优化后提示词。\n请注意你的回答中不需要包含除了优化后提示词'
        f'以外的任何文本，不需要打招呼，严格执行命令。\n原始提示词：{prompt}\n测试文本：{testText}\n模型输出结果：{extractResult}\n再次声明，输出'
        f'结果中包含且仅包含优化后提示词。保留原始提示词最末尾的"[待插入新闻文本]"。')

    messages = [{"role": "user", "content": evalPrompt}]
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages
    )
    optimizedPrompt = response.choices[0].message.content

    return optimizedPrompt


def optimize(apiKey, promptDictPath, testTextList, resultPath):
    with open(promptDictPath, 'r', encoding='utf-8') as f:
        promptDict: dict = json.load(f)

    for idx, prompt in promptDict.items():
        for testText in testTextList:
            myClient = OpenAI(api_key=apiKey, base_url='https://api.deepseek.com')
            prompt = singleRound(myClient, prompt, testText)
        promptDict[idx] = prompt
    with open(resultPath, 'w', encoding='utf-8') as f:
        json.dump(promptDict, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    api_key = 'sk-bb48574e9793409f9f9cbdb5370c55e3'
    promptDictPath = r'..\Data\OptimizePrompt\原始提示词.txt'
    testTextListPath = r'..\Data\OptimizePrompt\test_news.txt'
    resultPath = r'..\Data\OptimizePrompt\优化后提示词.txt'
    with open(testTextListPath, 'r', encoding='utf-8') as js:
        testTextListOri = json.load(js)
    testTextList = []
    for testTxt in testTextListOri:
        text = '标题：'+testTxt['title']+'\n'+'正文：'+testTxt['content']+'\n'
        testTextList.append(text)
    optimize(apiKey=api_key,promptDictPath=promptDictPath,testTextList=testTextList,resultPath=resultPath)

