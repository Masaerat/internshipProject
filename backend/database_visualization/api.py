import os
import sys

from flask import Flask, request, jsonify
from flask_cors import CORS
from Utils.MySqlHelper import MySqlHelper
from collections import Counter, defaultdict

app = Flask(__name__)
CORS(app)

# TODO: 替换为你的数据库连接信息
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # 替换为你的数据库密码
    'database': 'intershipproject',  # 替换为你的数据库名
    'port': 3306,
    'charset': 'utf8mb4'
}


class MovieAPI:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_rank_range(self):
        try:
            rank_min = int(request.args.get('rank_min', 1))
            rank_max = int(request.args.get('rank_max', 100))
            return rank_min, rank_max
        except Exception:
            return 1, 100

    def success(self, data, msg="ok"):
        return jsonify({"success": True, "msg": msg, "data": data})

    def fail(self, msg="error", data=None):
        return jsonify({"success": False, "msg": msg, "data": data})

    def type_distribution(self):
        rank_min, rank_max = self.get_rank_range()
        sql = "SELECT type FROM douban_hot100_list WHERE `rank` BETWEEN %s AND %s"
        with MySqlHelper(**self.db_config) as db:
            rows = db.query(sql, (rank_min, rank_max))
        type_counter = Counter()
        for row in rows:
            types = [t.strip() for t in row['type'].split(',') if t.strip()]
            type_counter.update(types)
        result = [{'type': t, 'count': c} for t, c in type_counter.items()]
        return self.success(result)

    def region_distribution(self):
        rank_min, rank_max = self.get_rank_range()
        sql = "SELECT regions FROM douban_hot100_list WHERE `rank` BETWEEN %s AND %s"
        with MySqlHelper(**self.db_config) as db:
            rows = db.query(sql, (rank_min, rank_max))
        region_counter = Counter()
        for row in rows:
            regions = [r.strip() for r in row['regions'].split(',') if r.strip()]
            region_counter.update(regions)
        result = [{'region': r, 'count': c} for r, c in region_counter.items()]
        return self.success(result)

    def release_date_distribution(self):
        rank_min, rank_max = self.get_rank_range()
        sql = "SELECT release_date FROM douban_hot100_list WHERE `rank` BETWEEN %s AND %s"
        with MySqlHelper(**self.db_config) as db:
            rows = db.query(sql, (rank_min, rank_max))
        period_counter = defaultdict(int)
        for row in rows:
            date_str = row['release_date']
            try:
                year = int(date_str[:4])
                period_start = year - (year % 5)
                period = f"{period_start}-{period_start + 4}"
                period_counter[period] += 1
            except Exception:
                continue
        result = [{'period': p, 'count': c} for p, c in sorted(period_counter.items())]
        return self.success(result)

    def score_distribution(self):
        rank_min, rank_max = self.get_rank_range()
        sql = "SELECT title, release_date, score FROM douban_hot100_list WHERE `rank` BETWEEN %s AND %s"
        with MySqlHelper(**self.db_config) as db:
            rows = db.query(sql, (rank_min, rank_max))
        result = [
            {'title': row['title'], 'release_date': row['release_date'], 'score': float(row['score'])}
            for row in rows
        ]
        return self.success(result)

    def actor_popularity(self):
        rank_min, rank_max = self.get_rank_range()
        sql = "SELECT actors FROM douban_hot100_list WHERE `rank` BETWEEN %s AND %s"
        with MySqlHelper(**self.db_config) as db:
            rows = db.query(sql, (rank_min, rank_max))
        actor_counter = Counter()
        for row in rows:
            actors = [a.strip() for a in row['actors'].split(',') if a.strip()]
            actor_counter.update(actors)
        result = [{'actor': a, 'count': c} for a, c in actor_counter.most_common(50)]  # 只返回前50
        return self.success(result)


movie_api = MovieAPI(db_config)


@app.errorhandler(Exception)
def handle_exception(e):
    return movie_api.fail(str(e)), 500


@app.route('/api/type-distribution')
def type_distribution():
    try:
        return movie_api.type_distribution()
    except Exception as e:
        return movie_api.fail(str(e)), 500


@app.route('/api/region-distribution')
def region_distribution():
    try:
        return movie_api.region_distribution()
    except Exception as e:
        return movie_api.fail(str(e)), 500


@app.route('/api/release-date-distribution')
def release_date_distribution():
    try:
        return movie_api.release_date_distribution()
    except Exception as e:
        return movie_api.fail(str(e)), 500


@app.route('/api/score-distribution')
def score_distribution():
    try:
        return movie_api.score_distribution()
    except Exception as e:
        return movie_api.fail(str(e)), 500


@app.route('/api/actor-popularity')
def actor_popularity():
    try:
        return movie_api.actor_popularity()
    except Exception as e:
        return movie_api.fail(str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)
