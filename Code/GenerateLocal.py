import copy
import os
import time
import requests
import json


def generate_with_ollama(prompt: str, model):
    # 构建请求体
    payload = {
        "model": model,  # 你可以换成任何你本地有的模型
        "prompt": prompt
    }

    try:
        with requests.post(OLLAMA_API_URL, json=payload) as response:
            response.raise_for_status()  # 如果请求失败（如404, 500），则抛出异常
            full_response = ''
            for line in response.iter_lines():
                if line:
                    content = json.loads(line.decode('utf-8'))
                    full_response += content['response']
            return full_response

    except requests.exceptions.RequestException as e:
        print(f"\n[错误] 无法连接到Ollama API: {e}")
    except json.JSONDecodeError as e:
        print(f"\n[错误] 解析JSON响应失败: {e}")


def generate(model, promptDict: dict, newsPath, resultPath):
    if not os.path.exists(resultPath):
        os.makedirs(resultPath, exist_ok=False)
    for promptidx, prompt in promptDict.items():
        for root, _, files in os.walk(newsPath):
            for file in files:
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    newsText = json.load(f)
                newsText = '标题：' + newsText['title'] + '\n' + '正文：' + newsText['content'] + '\n'
                tempPrompt = copy.deepcopy(prompt)
                tempPrompt = tempPrompt.replace("[待插入新闻文本]", newsText)
                extractResult = generate_with_ollama(tempPrompt, model)
                savePath = os.path.join(resultPath, '事件要素_' + file.replace('新闻', str(model).replace(':','-'))
                                        .replace('.txt', '_' + promptidx + '.txt'))
                with open(savePath, 'w+', encoding='utf-8') as f:
                    json.dump(extractResult, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # Ollama API的URL
    OLLAMA_API_URL = "http://localhost:11435/api/generate"
    modelList = ['llama3.1:8b', 'qwen3:latest', 'deepseek-r1:8b']
    promptDictPath = r'..\Data\OptimizePrompt\优化后提示词.txt'
    with open(promptDictPath, 'r', encoding='utf-8') as f:
        promptDict = json.load(f)
    newsPath = r'..\Data\新闻'
    resultPath = r'..\Data\ExtractResult'
    for model in modelList:
        generate(model, promptDict, newsPath, resultPath)
        time.sleep(60)
