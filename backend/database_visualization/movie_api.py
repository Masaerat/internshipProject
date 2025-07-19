from flask import request, jsonify
from Utils.MySqlHelper import MySqlHelper
from collections import Counter, defaultdict

class MovieAPI:
    """电影数据可视化API类"""
    
    def __init__(self, db_config):
        """
        初始化电影API
        
        Args:
            db_config: 数据库配置字典
        """
        self.db_config = db_config

    def get_rank_range(self):
        """获取rank范围参数"""
        try:
            rank_min = int(request.args.get('rank_min', 1))
            rank_max = int(request.args.get('rank_max', 100))
            return rank_min, rank_max
        except Exception:
            return 1, 100

    def success(self, data, msg="ok"):
        """成功响应"""
        return jsonify({"success": True, "msg": msg, "data": data})

    def fail(self, msg="error", data=None):
        """失败响应"""
        return jsonify({"success": False, "msg": msg, "data": data})

    def type_distribution(self):
        """类型分布接口"""
        try:
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
        except Exception as e:
            return self.fail(str(e))

    def region_distribution(self):
        """地区分布接口"""
        try:
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
        except Exception as e:
            return self.fail(str(e))

    def release_date_distribution(self):
        """上映时间分布接口"""
        try:
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
                    period = f"{period_start}-{period_start+4}"
                    period_counter[period] += 1
                except Exception:
                    continue
            result = [{'period': p, 'count': c} for p, c in sorted(period_counter.items())]
            return self.success(result)
        except Exception as e:
            return self.fail(str(e))

    def score_distribution(self):
        """评分分布接口"""
        try:
            rank_min, rank_max = self.get_rank_range()
            sql = "SELECT title, release_date, score FROM douban_hot100_list WHERE `rank` BETWEEN %s AND %s"
            with MySqlHelper(**self.db_config) as db:
                rows = db.query(sql, (rank_min, rank_max))
            result = [
                {'title': row['title'], 'release_date': row['release_date'], 'score': float(row['score'])}
                for row in rows
            ]
            return self.success(result)
        except Exception as e:
            return self.fail(str(e))

    def actor_popularity(self):
        """演员热度接口"""
        try:
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
        except Exception as e:
            return self.fail(str(e)) 