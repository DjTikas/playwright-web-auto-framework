import os

import pytest
#
# def test_demo(page): # 注意参数是page，插件原生fixture
#     assert False


if __name__ == '__main__':
    # 运行测试用例
    pytest.main(['./cases/test_project', '--alluredir', './reports'])
    # pytest.main(['./cases/test_auth', '--alluredir', './reports'])1
    # pytest.main(['--alluredir', './reports'])
    # 生成测试报告
    os.system('allure generate ./reports -o ./allure_report --clean --lang zh')
    # 打开测试报告
    # os.system('allure serve ./reports')