from typing import List, Union, Dict, Tuple

import pymysql


class MySqlHelper:
    from typing import Optional, Any, Type
    from pymysql.cursors import Cursor, DictCursor

    def __init__(
            self,
            host: Optional[str],  # 允许 None
            user: Optional[str],  # 允许 None
            password: Optional[str],  # 允许 None
            database: Optional[str],  # 允许 None
            port: int = 3306,
            charset: str = 'utf8mb4',
            cursor_class: Optional[Type[Cursor]] = DictCursor,  # 允许 None，默认 DictCursor
    ):
        """初始化数据库连接

        Args:
            host: 数据库主机地址（可选）
            user: 数据库用户名（可选）
            password: 数据库密码（可选）
            database: 数据库名称（可选）
            port: 数据库端口，默认为3306
            charset: 字符集，默认为utf8mb4
            cursor_class: 游标类型，默认为 DictCursor
        """
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            charset=charset,
            cursorclass=cursor_class,
        )
        self.cursor = self.connection.cursor()

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时自动关闭连接"""
        self.close()

    # 底层核心方法
    def _execute(self, query: str, params=None, many: bool = False) -> bool:
        """底层执行方法（私有方法）

        Args:
            query: SQL语句
            params: 参数，可以是单条(tuple/dict)或多条(List)
            many: 是否批量操作

        Returns:
            执行是否成功
        """
        try:
            if many:
                self.cursor.executemany(query, params)
            else:
                self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"操作执行失败: {e}")
            self.connection.rollback()
            return False

    def _query(self, query: str, params=None, fetch_all: bool = True):
        """底层查询方法（私有方法）

        Args:
            query: SQL查询语句
            params: 查询参数
            fetch_all: 是否获取所有结果

        Returns:
            查询结果或None(出错时)
        """
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall() if fetch_all else self.cursor.fetchone()
        except Exception as e:
            print(f"查询执行失败: {e}")
            return None

    # 公开的单条操作方法
    def execute(self, query: str, params: Union[Tuple, Dict[str, Any]] = None) -> bool:
        """执行单条SQL操作(增删改)

        Args:
            query: SQL语句
            params: 参数(tuple或dict)

        Returns:
            执行是否成功
        """
        return self._execute(query, params, many=False)

    def query(self, query: str, params: Union[Tuple, Dict[str, Any]] = None) -> Optional[List[Dict]]:
        """执行查询并返回所有结果

        Args:
            query: SQL查询语句
            params: 查询参数

        Returns:
            查询结果列表或None(出错时)
        """
        return self._query(query, params, fetch_all=True)

    def query_one(self, query: str, params: Union[Tuple, Dict[str, Any]] = None) -> Optional[Dict]:
        """执行查询并返回第一条结果

        Args:
            query: SQL查询语句
            params: 查询参数

        Returns:
            单条查询结果或None(出错时)
        """
        return self._query(query, params, fetch_all=False)

    def insert(self, query: str, params: Union[Tuple, Dict[str, Any]]) -> bool:
        """插入单条数据

        Args:
            query: SQL插入语句
            params: 插入数据

        Returns:
            是否插入成功
        """
        return self.execute(query, params)

    def update(self, query: str, params: Union[Tuple, Dict[str, Any]]) -> bool:
        """更新单条数据

        Args:
            query: SQL更新语句
            params: 更新参数

        Returns:
            是否更新成功
        """
        return self.execute(query, params)

    def delete(self, query: str, params: Union[Tuple, Dict[str, Any]]) -> bool:
        """删除单条数据

        Args:
            query: SQL删除语句
            params: 删除条件参数

        Returns:
            是否删除成功
        """
        return self.execute(query, params)

    # 公开的批量操作方法
    def execute_many(self, query: str, params_list: List[Union[Tuple, Dict[str, Any]]]) -> bool:
        """批量执行SQL操作(增删改)

        Args:
            query: SQL语句
            params_list: 参数列表

        Returns:
            执行是否成功
        """
        return self._execute(query, params_list, many=True)

    def insert_many(self, query: str, params_list: List[Union[Tuple, Dict[str, Any]]]) -> bool:
        """批量插入数据

        Args:
            query: SQL插入语句
            params_list: 多条插入数据的列表

        Returns:
            是否批量插入成功
        """
        return self.execute_many(query, params_list)

    def update_many(self, query: str, params_list: List[Union[Tuple, Dict[str, Any]]]) -> bool:
        """批量更新数据

        Args:
            query: SQL更新语句
            params_list: 多条更新参数的列表

        Returns:
            是否批量更新成功
        """
        return self.execute_many(query, params_list)

    def delete_many(self, query: str, params_list: List[Union[Tuple, Dict[str, Any]]]) -> bool:
        """批量删除数据

        Args:
            query: SQL删除语句
            params_list: 多条删除条件的列表

        Returns:
            是否批量删除成功
        """
        return self.execute_many(query, params_list)

    def close(self) -> None:
        """关闭数据库连接"""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
