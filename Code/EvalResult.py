import json
from openai import OpenAI


def singleRound(client, testText, extractResult):
    # return optimized prompt
    evalPrompt = (
        f'你目前从事事件要素抽取方面的工作，并且你是这个领域的专家。\n你的任务是：首先仔细阅读给出的测试文本和事件要素抽取结果，然后根据你的经验'
        f'评估这个抽取结果的效果，最后给出评分和简短的点评。\n输出结果为且仅为一个json，格式为{{"score":[0.0-10.0](根据具体得分变化),"comment":(根据具体情况点评)}}\n'
        f'测试文本：{testText}\n模型输出结果：{extractResult}\n再次声明，输出结果为且仅为一个json')

    messages = [{"role": "user", "content": evalPrompt}]
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages
    )
    result = response.choices[0].message.content

    return result


def evalResult(apiKey, testTextList, extractResultList, evalResultPath):
    evalResultList = []
    idx = 1
    for testText,extractResult in zip(testTextList, extractResultList):
        myClient = OpenAI(api_key=apiKey, base_url='https://api.deepseek.com')
        evalRes = singleRound(myClient, testText, extractResult)
        evalRes = json.loads(evalRes)
        evalResultList.append({idx: evalRes})
        idx += 1

    with open(evalResultPath, 'w', encoding='utf-8') as f:
        json.dump(evalResultList, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    api_key = 'sk-bb48574e9793409f9f9cbdb5370c55e3'
