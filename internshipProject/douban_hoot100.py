import json
import urllib.response
import urllib.parse
import urllib.request
from MySqlHelper import MySqlHelper


def get_douban_content(page):
    url = ' https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action='

    headers = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 '
            'Safari/537.36'
    }
    data = {
        'start': (page - 1) * 20,
        'limit': 20
    }
    data = urllib.parse.urlencode(data)
    url = url + data
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content


def get_douban_list():
    # 这里选择要输入的起始和结束页码 如果只爬取100条的话 start_page = 0 end_page = 5
    start_page = int(input("请输入起始的页码"))
    end_page = int(input("请输入结束的页码"))
    douban_list = []
    for page in range(start_page, end_page + 1):
        content = get_douban_content(page)
        data = json.loads(content)
        for index, movie in enumerate(data):
            global_rank = (page - start_page) * 20 + index + 1  # 计算全局排名
            movie_tuple = (
                global_rank,
                ", ".join(movie["types"]),  # type
                ", ".join(movie["regions"]),  # regions
                movie["title"],  # title
                movie["release_date"],  # release_date
                movie["score"],  # score (转换为float)
                ", ".join(movie["actors"])  # actors
            )
            douban_list.append(movie_tuple)
    return douban_list


# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # 替换为你的数据库密码
    'database': 'intershipproject',  # 替换为你的数据库名
    'port': 3306,
    'charset': 'utf8mb4'
}

# 创建对应的数据库表
# 为了可视化的服务 我设计的字段分别为：rank, types, regions, title, release_date, score, actors
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS douban_hot100_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `rank` INT,
    `type` TEXT,
    regions TEXT,
    title VARCHAR(100),
    release_date VARCHAR(20),
    score VARCHAR(5),
    actors TEXT
)
"""

INSERT_SQL = "INSERT INTO douban_hot100_list (`rank`,`type`, regions , title , release_date , score , actors) VALUES (%s, %s, %s, %s, %s, %s, %s)"


def store_douban_hot100():
    douban_list = get_douban_list()

    # 初始化数据库连接
    helper = MySqlHelper(**DB_CONFIG)

    # 创建测试表
    helper.execute(CREATE_TABLE_SQL)

    # 插入到数据库中
    helper.insert_many(INSERT_SQL, douban_list)


if __name__ == '__main__':
    store_douban_hot100()
