import pytest
from playwright.sync_api import Browser, BrowserContext
from pytest_playwright.pytest_playwright import browser
from typing import Dict, Any

from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def session_shared_context(browser: Browser, browser_context_args: dict, pytestconfig):
    """
    session生命周期：全局唯一BrowserContext，不随每条用例销毁
    所有业务用例共用这个上下文，HTTP缓存、cookie驻留内存，打开页面速度快
    """
    ctx = browser.new_context(**browser_context_args)
    yield ctx
    # 测试全部跑完最后才关闭上下文
    ctx.close()


@pytest.fixture(scope="session")
def login_prepare(session_shared_context: BrowserContext, base_url, pytestconfig):
    """session内执行一次登录，cookie保存在session_shared_context内存中，不写磁盘文件"""
    page = session_shared_context.new_page()
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("daij", "aa123456")
    page.wait_for_url("**/index.html")
    page.close()
    yield


@pytest.fixture
def shared_page(session_shared_context: BrowserContext):
    """
    给业务用例使用：每条用例生成全新标签页page，上下文复用session_shared_context
    用例结束只关闭标签页，context本身存活，缓存、cookie保留
    """
    p = session_shared_context.new_page()
    yield p
    p.close()

"""
    下面这个方案可以实现登录一次后保存上下文，
    然后加载到browser_context_args里面，
    但是因为现在版本内置的context是function级别的，
    每条用例执行一次都会销毁然后再生成，速度很慢
"""

#
# @pytest.fixture(scope="session")
# def login_save_auth(browser, base_url, pytestconfig):
#     """全局登录一次，保存cookie"""
#     context = browser.new_context(base_url=base_url)
#     page = context.new_page()
#     LoginPage(page).navigate()
#     LoginPage(page).login('daij', 'aa123456')
#     # 等待页面重定向
#     page.wait_for_url(url='**/index.html')
#     # 保存storage state到指定的文件
#     storage_path = pytestconfig.rootpath.joinpath('auth/state.json')
#     context.storage_state(path=storage_path)
#     context.close()
#
# # 重写覆盖browser_context_args
# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args, playwright, pytestconfig):
#     """
#     添加context上下文参数默认每个页面加载cookies
#     :param browser_context_args:
#     :param playwright:
#     :param pytestconfig:
#     :return:
#     """
#     return {
#         "storage_state": pytestconfig.rootpath.joinpath('auth/state.json'),
#         **browser_context_args,
#     }

@pytest.fixture(scope="module")
def unlogin_context(browser, base_url, pytestconfig, browser_context_args: Dict):
    """
    登录、注册页面（不依赖于先登录）单独创建独立的 context 上下文
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