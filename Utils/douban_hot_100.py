import json
import urllib.parse
import urllib.request
from MySqlHelper import MySqlHelper


class DoubanMovieScraper:
    def __init__(self, db_config=None):
        self.base_url = 'https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        self.db_config = db_config or {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'intershipproject',
            'port': 3306,
            'charset': 'utf8mb4'
        }
        self.db_helper = None

    def _fetch_page_data(self, page, page_size=20):
        """获取单页电影数据"""
        data = {
            'start': (page - 1) * page_size,
            'limit': page_size
        }
        query_string = urllib.parse.urlencode(data)
        url = self.base_url + query_string

        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        return response.read().decode('utf-8')

    def _parse_movie_data(self, raw_data, start_page, current_page):
        """解析原始电影数据"""
        movies = json.loads(raw_data)
        parsed_movies = []

        for index, movie in enumerate(movies):
            global_rank = (current_page - start_page) * 20 + index + 1
            parsed_movies.append((
                global_rank,
                ", ".join(movie["types"]),
                ", ".join(movie["regions"]),
                movie["title"],
                movie["release_date"],
                movie["score"],
                ", ".join(movie["actors"])
            ))
        return parsed_movies

    def _initialize_database(self):
        """初始化数据库表结构"""
        create_table_sql = """
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
        self.db_helper.execute(create_table_sql)

    def scrape_movies(self, start_page, end_page):
        """爬取指定页码范围的电影数据"""
        all_movies = []

        for page in range(start_page, end_page + 1):
            raw_data = self._fetch_page_data(page)
            page_movies = self._parse_movie_data(raw_data, start_page, page)
            all_movies.extend(page_movies)

        return all_movies

    def store_to_database(self, movies):
        """将电影数据存储到数据库"""
        if not self.db_helper:
            self.db_helper = MySqlHelper(**self.db_config)
            self._initialize_database()

        insert_sql = """
        INSERT INTO douban_hot100_list 
        (`rank`, `type`, regions, title, release_date, score, actors) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.db_helper.insert_many(insert_sql, movies)

    def run(self):
        """运行爬虫主流程"""
        try:
            start_page = int(input("请输入起始页码: "))
            end_page = int(input("请输入结束页码: "))

            movies = self.scrape_movies(start_page, end_page)
            self.store_to_database(movies)

            print(f"成功爬取并存储了 {len(movies)} 条电影数据")
        except ValueError:
            print("请输入有效的页码数字")
        except Exception as e:
            print(f"发生错误: {str(e)}")


if __name__ == '__main__':
    scraper = DoubanMovieScraper()
    scraper.run()
