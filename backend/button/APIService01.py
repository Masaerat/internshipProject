from flask import request, Flask


class APIService01:
    def __init__(self):
        self.app = Flask(__name__)
        self._setup_routes()

    def _setup_routes(self):
        """设置所有路由"""
        self.app.add_url_rule(
            '/api/get-example',
            'get_example',
            self._handle_get_example,
            methods=['GET']
        )

        self.app.add_url_rule(
            '/api/post-example',
            'post_example',
            self._handle_post_example,
            methods=['POST']
        )

    def run(self, **kwargs):
        """运行应用"""
        self.app.run(**kwargs)

    def _handle_get_example(self):
        """处理GET请求"""
        param = request.args.get('param', '')
        return f"参数是{param}"

    def _handle_post_example(self):
        """处理POST请求"""
        # 获取URL参数
        url_param = request.args.get('param', '')
        # 获取body参数
        body_data = request.get_json()
        body_param = body_data.get('bodyParam', '') if body_data else ''
        return f"body中的参数是{body_param}，param中的参数是{url_param}"


# 使用示例
if __name__ == '__main__':
    api = APIService01()
    api.run(debug=True)
