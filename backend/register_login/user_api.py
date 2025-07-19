from flask import request, jsonify
import bcrypt
import jwt
import datetime
from functools import wraps
from Utils.MySqlHelper import MySqlHelper


class UserAPI:
    def __init__(self, db_config, jwt_secret='your-secret-key'):
        """
        初始化用户API
        
        Args:
            db_config: 数据库配置字典
            jwt_secret: JWT密钥
        """
        self.db_config = db_config
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = 'HS256'

    def success(self, data, msg="ok"):
        """成功响应"""
        return jsonify({"success": True, "msg": msg, "data": data})

    def fail(self, msg="error", data=None):
        """失败响应"""
        return jsonify({"success": False, "msg": msg, "data": data})

    def hash_password(self, password):
        """密码加密"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password, hashed):
        """密码验证"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def generate_token(self, user_id, username):
        """生成JWT token"""
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 7天过期
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def verify_token(self, token):
        """验证JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def register(self):
        """用户注册"""
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            email = data.get('email', '')
            phone = data.get('phone', '')

            # 参数验证
            if not username or not password:
                return self.fail("用户名和密码不能为空")

            if len(username) < 3 or len(username) > 20:
                return self.fail("用户名长度必须在3-20个字符之间")

            if len(password) < 6:
                return self.fail("密码长度不能少于6个字符")

            # 检查用户名是否已存在
            with MySqlHelper(**self.db_config) as db:
                check_sql = "SELECT id FROM users WHERE username = %s"
                existing_user = db.query_one(check_sql, (username,))
                if existing_user:
                    return self.fail("用户名已存在")

                # 密码加密
                hashed_password = self.hash_password(password)

                # 插入新用户
                insert_sql = "INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)"
                if db.insert(insert_sql, (username, hashed_password, email, phone)):
                    return self.success(None, "注册成功")
                else:
                    return self.fail("注册失败")

        except Exception as e:
            return self.fail(str(e))

    def login(self):
        """用户登录"""
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return self.fail("用户名和密码不能为空")

            # 查询用户
            with MySqlHelper(**self.db_config) as db:
                sql = "SELECT id, username, password FROM users WHERE username = %s"
                user = db.query_one(sql, (username,))

                if not user:
                    return self.fail("用户名或密码错误")

                # 验证密码
                if not self.check_password(password, user['password']):
                    return self.fail("用户名或密码错误")

                # 生成token
                token = self.generate_token(user['id'], user['username'])

                return self.success({
                    'token': token,
                    'user_id': user['id'],
                    'username': user['username']
                }, "登录成功")

        except Exception as e:
            return self.fail(str(e))

    def get_user_info(self):
        """获取用户信息"""
        try:
            # 从请求头获取token
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return self.fail("未提供有效的认证token")

            token = auth_header.split(' ')[1]
            payload = self.verify_token(token)

            if not payload:
                return self.fail("token已过期或无效")

            # 查询用户信息
            with MySqlHelper(**self.db_config) as db:
                sql = "SELECT id, username, email, phone, created_at FROM users WHERE id = %s"
                user = db.query_one(sql, (payload['user_id'],))

                if not user:
                    return self.fail("用户不存在")

                return self.success({
                    'user_id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'phone': user['phone'],
                    'created_at': user['created_at'].strftime('%Y-%m-%d %H:%M:%S') if user['created_at'] else None
                })

        except Exception as e:
            return self.fail(str(e))

    def logout(self):
        """用户登出"""
        # JWT是无状态的，客户端删除token即可
        return self.success(None, "登出成功")

    def require_auth(self, f):
        """认证装饰器"""

        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return self.fail("未提供有效的认证token"), 401

            token = auth_header.split(' ')[1]
            payload = self.verify_token(token)

            if not payload:
                return self.fail("token已过期或无效"), 401

            # 将用户信息添加到请求上下文
            request.user = payload
            return f(*args, **kwargs)

        return decorated_function

    def get_auth_decorator(self):
        """获取认证装饰器"""
        return self.require_auth
