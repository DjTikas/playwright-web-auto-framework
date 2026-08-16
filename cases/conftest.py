import pytest
from pytest_playwright.pytest_playwright import browser
from typing import Dict, Any


"""
    我只写了登录注册页面的context和page，并且删去了很多功能
"""

@pytest.fixture(scope="module")
def unlogin_context(browser, base_url, pytestconfig, browser_context_args: Dict):
    """
    登录注册页面（不依赖于先登录）单独创建独立的 context 上下文
    避免全局先登录加载cookie，导致有些打开登录页直接跳到首页去了
    :return:

    1）browser
    来源：pytest‑playwright 内置 fixture，session 级别，已经启动好的浏览器实例。
    拿来干什么：调用 browser.new_context()，创建 BrowserContext 隔离环境。
    2）base_url
    pytest‑playwright 内置 fixture，没有使用，纯粹做依赖声明。
    3）pytestconfig
    pytest 内置 fixture，没有使用，向下游的unlogin_page做依赖链传递。
    4）browser_context_args
    来源：上面那个钩子 fixture 输出的配置字典。
    拿来干什么：**browser_context_args 解包，传给 new_context，把窗口、证书的配置全部带进去。
    """
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()

@pytest.fixture(scope="function")
def unlogin_page(unlogin_context, pytestconfig: Any, request: pytest.FixtureRequest):
    """
    登录注册页面（不依赖于先登录）单独创建独立的 page 对象
    带上用例失败截图和添加视频功能

    1）unlogin_context
    上一级 fixture unlogin_context yield 返回
    隔离浏览器环境，执行 unlogin_context.new_page() 创建页面；同时绑定页面事件监听 .on("page")
    2）pytestconfig
    pytest 内置 fixture，截图时用上
    读取命令行参数，调用工具函数等
    3）request
    pytest 内置 fixture
    获取当前用例执行成功 / 失败，截图时用上
    """
    unlogin_page = unlogin_context.new_page()
    yield unlogin_page
    unlogin_page.close()