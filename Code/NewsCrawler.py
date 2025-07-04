import requests
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import quote


def crawl_xinhua_search(keyword_all, keyword_one, max_pages=3):
    """爬取新华网搜索结果的新闻"""
    base_url = "https://so.news.cn/getNews/"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,de-DE;q=0.6,de;q=0.5",
        "Connection": "keep-alive",
        "Cookie": "wdcid=08d862e9578163d9; wdlast=1751618319",
        "Host": "search.news.cn",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    results = []

    for page in range(1, max_pages + 1):
        # 构造请求数据
        params = {
            "keyword": keyword_all,
            "keyWordAll": keyword_all,
            "keyWordOne": keyword_one,
            "searchFields": 0,
            "senSearch": 1,
            "curPage": page,
            "sortField": 1,
            "lang": "cn",
            "url": "news.cn"
        }
        #
        headers['Referer'] = "https://so.news.cn/?keyWordAll={}&keyWordOne={}&searchFields={}&sortField={}&url={}&lang={}&senSearch={}".format(
            quote(params["keyWordAll"].replace(' ', '+')),
            quote(params['keyWordOne'].replace(' ', '+')),
            params["searchFields"],
            params["sortField"],
            params["url"],
            params["lang"],
            params["senSearch"])
        try:
            # 发送POST请求
            response = requests.get(
                base_url,
                headers=headers,
                params=params,
                timeout=15
            )
            response.raise_for_status()

            # 解析JSON数据
            data = response.json()
            for item in data.get("content", {}).get("results", []):
                news = {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "pub_time": item.get("pubtime"),
                    "source": item.get("sitename"),
                    "content": get_news_content(item.get("url"))  # 获取正文
                }
                results.append(news)
                print(f"已爬取: {news['title']} | {news['pub_time']}")

            print(f"第 {page} 页完成，共 {len(data['content']['results'])} 条结果")
            time.sleep(2)  # 礼貌性延迟

        except Exception as e:
            print(f"第 {page} 页请求失败: {str(e)}")

    return results


def get_news_content(url):
    """获取新闻正文内容"""
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=8
        )
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取正文内容
        content_div = soup.find('span', id='detailContent')
        paragraphs = [p.text.strip() for p in content_div.find_all('p')]
        content = '\n'.join(paragraphs)
        return content

    except Exception as e:
        return f"内容获取失败: {str(e)}"


if __name__ == "__main__":
    keyword_all = "科技 风险 挑战"
    keyword_one = "出口管制 经济制裁 金融限制 贸易摩擦 市场壁垒 人才封锁"

    # 开始爬取（最多3页）
    news_data = crawl_xinhua_search(keyword_all, keyword_one, max_pages=5)

    # 保存结果
    with open(f"../新闻/xinhua_news_{keyword_all}.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)

    print(f"爬取完成！共获取 {len(news_data)} 条新闻，已保存至JSON文件")
