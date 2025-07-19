import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Utils')))
from flask import Flask
from flask_cors import CORS
from movie_api import MovieAPI
from backend.register_login.user_api import UserAPI

app = Flask(__name__)
CORS(app)  # 启用跨域支持

# TODO: 替换为你的数据库连接信息
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # 替换为你的数据库密码
    'database': 'intershipproject',  # 替换为你的数据库名
    'port': 3306,
    'charset': 'utf8mb4'
}

# 创建API实例
movie_api = MovieAPI(db_config)
user_api = UserAPI(db_config)

# 获取认证装饰器
require_auth = user_api.get_auth_decorator()

@app.errorhandler(Exception)
def handle_exception(e):
    """全局异常处理"""
    return movie_api.fail(str(e)), 500

# ==================== 电影数据可视化接口 ====================
@app.route('/api/type-distribution')
def type_distribution():
    """类型分布接口"""
    try:
        return movie_api.type_distribution()
    except Exception as e:
        return movie_api.fail(str(e)), 500

@app.route('/api/region-distribution')
def region_distribution():
    """地区分布接口"""
    try:
        return movie_api.region_distribution()
    except Exception as e:
        return movie_api.fail(str(e)), 500

@app.route('/api/release-date-distribution')
def release_date_distribution():
    """上映时间分布接口"""
    try:
        return movie_api.release_date_distribution()
    except Exception as e:
        return movie_api.fail(str(e)), 500

@app.route('/api/score-distribution')
def score_distribution():
    """评分分布接口"""
    try:
        return movie_api.score_distribution()
    except Exception as e:
        return movie_api.fail(str(e)), 500

@app.route('/api/actor-popularity')
def actor_popularity():
    """演员热度接口"""
    try:
        return movie_api.actor_popularity()
    except Exception as e:
        return movie_api.fail(str(e)), 500

# ==================== 用户认证接口 ====================
@app.route('/api/register', methods=['POST'])
def register():
    """用户注册接口"""
    try:
        return user_api.register()
    except Exception as e:
        return user_api.fail(str(e)), 500

@app.route('/api/login', methods=['POST'])
def login():
    """用户登录接口"""
    try:
        return user_api.login()
    except Exception as e:
        return user_api.fail(str(e)), 500

@app.route('/api/user-info', methods=['GET'])
@require_auth
def get_user_info():
    """获取用户信息接口"""
    try:
        return user_api.get_user_info()
    except Exception as e:
        return user_api.fail(str(e)), 500

@app.route('/api/logout', methods=['POST'])
@require_auth
def logout():
    """用户登出接口"""
    try:
        return user_api.logout()
    except Exception as e:
        return user_api.fail(str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
