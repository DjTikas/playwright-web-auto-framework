import os
import shutil

import pytest
from pytest import Item
import allure
# import pytest
# from typing import Dict
#
# # 本地插件注册
# pytest_plugins = ['plugins.pytest_playwright']
# , 'plugins.pytest_base_url_plugin']
#

def pytest_runtest_call(item: Item):
    # 动态添加测试类的allure.feature()
    if item.parent._obj.__doc__:
        allure.dynamic.feature(item.parent._obj.__doc__)
    # 动态添加测试用例的title标题allure.title()
    if item.function.__doc__:
        allure.dynamic.title(item.function.__doc__)


def _clean_dir(dir_path: str):
    if os.path.exists(dir_path):
        for name in os.listdir(dir_path):
            full_path = os.path.join(dir_path, name)
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
    else:
        os.makedirs(dir_path, exist_ok=True)

@pytest.fixture(scope="session", autouse=True)
def clean_allure_env():
    """会话启动自动清理allure‑results和reports"""
    _clean_dir("test-results")
    _clean_dir("reports")
    yield

#
# # 重写插件钩子 1
# # 生产参数字典，供给 pytest‑playwright 内部，用于启动浏览器。
# @pytest.fixture(scope="session")
# def browser_type_launch_args(browser_type_launch_args) -> Dict:
#     """窗口最大化"""
#     return {"args": ['--start-maximized'], **browser_type_launch_args}
#
#
# # 重写插件钩子 2
# # 生产参数字典，输出一个配置字典。
# # unlogin_context等固件会 消费这个字典
# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args, playwright, pytestconfig) -> Dict:
#     """窗口最大化"""
#     return {
#         "no_viewport": True,
#         # 忽略https报错
#         "ignore_https_errors": True,
#         **browser_context_args
#     }
