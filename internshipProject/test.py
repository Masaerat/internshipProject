from MySqlHelper import MySqlHelper

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # 替换为你的数据库密码
    'database': 'intershipproject',  # 替换为你的数据库名
    'port': 3306,
    'charset': 'utf8mb4'
}

# 测试表和数据
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS test_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT
)
"""
INSERT_TEST_DATA_SQL = "INSERT INTO test_table (name, age) VALUES (%s, %s)"
TEST_DATA = [
    ('Alice', 25),
    ('Bob', 30),
    ('Charlie', 35)
]
SELECT_ALL_SQL = "SELECT * FROM test_table"
SELECT_ONE_SQL = "SELECT * FROM test_table WHERE id = %s"
UPDATE_SQL = "UPDATE test_table SET age = %s WHERE id = %s"
DELETE_SQL = "DELETE FROM test_table WHERE id = %s"


def main():
    # 初始化数据库连接
    helper = MySqlHelper(**DB_CONFIG)

    # 创建测试表
    helper.execute(CREATE_TABLE_SQL)

    # 测试单条插入
    print("测试单条插入...")
    helper.insert(INSERT_TEST_DATA_SQL, TEST_DATA[0])
    result = helper.query_one(SELECT_ONE_SQL, (1,))
    print("查询结果:", result)
    assert result['name'] == TEST_DATA[0][0] and result['age'] == TEST_DATA[0][1]

    # 测试批量插入
    print("测试批量插入...")
    helper.insert_many(INSERT_TEST_DATA_SQL, TEST_DATA[1:])
    results = helper.query(SELECT_ALL_SQL)
    print("查询所有结果:", results)
    assert len(results) == len(TEST_DATA)

    # 测试更新单条数据
    print("测试更新单条数据...")
    helper.update(UPDATE_SQL, (40, 1))
    result = helper.query_one(SELECT_ONE_SQL, (1,))
    print("更新后查询结果:", result)
    assert result['age'] == 40

    # 测试批量更新数据
    print("测试批量更新数据...")
    update_data = [(50, 2), (60, 3)]
    helper.update_many(UPDATE_SQL, update_data)
    results = helper.query(SELECT_ALL_SQL)
    print("批量更新后查询结果:", results)
    for result in results:
        if result['id'] == 2:
            assert result['age'] == 50
        elif result['id'] == 3:
            assert result['age'] == 60

    # 测试删除单条数据
    print("测试删除单条数据...")
    helper.delete(DELETE_SQL, (1,))
    result = helper.query_one(SELECT_ONE_SQL, (1,))
    print("删除后查询结果:", result)
    assert result is None

    # 测试批量删除数据
    print("测试批量删除数据...")
    delete_ids = [(2,), (3,)]
    helper.delete_many(DELETE_SQL, delete_ids)
    results = helper.query(SELECT_ALL_SQL)
    print("批量删除后查询结果:", results)
    assert len(results) == 0

    # 关闭数据库连接
    helper.close()
    print("所有测试完成！")


if __name__ == "__main__":
    main()