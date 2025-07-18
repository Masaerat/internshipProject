import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json
from MySqlHelper import MySqlHelper


# 使用urllib实现
def get_baidu_hotsearch():
    # 百度热搜的API接口
    url = "https://top.baidu.com/board?tab=realtime"

    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }

    try:
        # 创建请求对象
        req = urllib.request.Request(url, headers=headers)

        # 发送请求并获取响应
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 查找热搜项目 - 根据百度风云榜的实际HTML结构调整
        hot_items = soup.find_all('div', class_='category-wrap_iQLoo')

        hot_list = []
        for index, item in enumerate(hot_items[:100], 1):
            title = item.find('div', class_='c-single-text-ellipsis').text.strip()
            hot_score = item.find('div', class_='hot-index_1Bl1a').text.strip()
            link = item.find('a')['href']

            hot_list.append((index, title, hot_score, link))

        return hot_list

    except Exception as e:
        print(f"获取百度热搜失败: {e}")
        return []


# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # 替换为你的数据库密码
    'database': 'intershipproject',  # 替换为你的数据库名
    'port': 3306,
    'charset': 'utf8mb4'
}

# 创建对应的数据库表 字段分别为：rank,title,hot_score,link
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS hot_search_01 (
        id INT AUTO_INCREMENT PRIMARY KEY ,
        `rank` INT  ,
        title VARCHAR(300),
        hot_score VARCHAR(50),
        link VARCHAR(300)
    )
"""

INSERT_SQL = "INSERT INTO hot_search_01 (`rank`, title, hot_score, link) VALUES (%s, %s, %s, %s)"


def store_hot_list():
    # 获取热搜
    hot_search = get_baidu_hotsearch()

    # 初始化数据库连接
    helper = MySqlHelper(**DB_CONFIG)

    # 创建测试表
    helper.execute(CREATE_TABLE_SQL)

    # 插入到数据库中
    helper.insert_many(INSERT_SQL, hot_search)


if __name__ == '__main__':
    store_hot_list()
