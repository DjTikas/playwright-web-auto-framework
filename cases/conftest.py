import os

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Error
from pytest_playwright.pytest_playwright import browser
from typing import Dict, Any, List

from slugify import slugify

from pages.login_page import LoginPage


def _build_artifact_test_folder(pytestconfig: Any, request: pytest.FixtureRequest, folder_or_file_name: str) -> str:
    output_dir = pytestconfig.getoption("--output")
    return os.path.join(output_dir, slugify(request.node.nodeid), folder_or_file_name)


@pytest.fixture(scope="session")
def login_prepare(context, base_url, pytestconfig) -> None:
    """有些网站网页关闭cookie就失效了，全局登录一次"""
    # context = browser.new_context(base_url=base_url, no_viewport=True)
    print("base_url----", base_url)
    page = context.new_page()
    LoginPage(page).navigate()
    LoginPage(page).login("py", "123456")
    # 等待登录成功页面重定向
    page.wait_for_url(url='**/index.html')


@pytest.fixture(scope="module")
def unlogin_context(browser, base_url, pytestconfig, browser_context_args: Dict):
    """
    登录注册页面（不依赖于先登录）单独创建独立的 context 上下文
    避免全局先登录加载cookie，导致有些打开登录页直接跳到首页去了
    :return:
    """
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture
def unlogin_page(unlogin_context: BrowserContext, pytestconfig: Any, request: pytest.FixtureRequest):
    """
    登录注册页面（不依赖于先登录）单独创建独立的 page 对象
    带上用例失败截图和添加视频功能
    """
    pages: List[Page] = []
    unlogin_context.on("page", lambda page: pages.append(page))
    page = unlogin_context.new_page()
    yield page
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else True
    # 截图判断
    screenshot_option = pytestconfig.getoption("--screenshot")
    capture_screenshot = screenshot_option == "on" or (failed and screenshot_option == "only-on-failure")
    print(f"capture_screenshot:{capture_screenshot}")
    if capture_screenshot:
        for index, page in enumerate(pages):
            human_readable_status = "failed" if failed else "finished"
            screenshot_path = _build_artifact_test_folder(
                pytestconfig, request, f"test-{human_readable_status}-{index + 1}.png"
            )
            print(f'-----------------{screenshot_path}')
            try:
                page.screenshot(timeout=5000, path=screenshot_path)
                # 把截图放入allure报告
                allure.attach.file(screenshot_path,
                                   name=f"{request.node.name}-{human_readable_status}-{index + 1}",
                                   attachment_type=allure.attachment_type.PNG
                                   )
            except Error:
                pass
    page.close()
    # 用例添加视频
    video_option = pytestconfig.getoption("--video")
    preserve_video = video_option == "on" or (failed and video_option == "retain-on-failure")
    if preserve_video:
        for page in pages:
            video = page.video
            if not video:
                continue
            try:
                video_path = video.path()
                file_name = os.path.basename(video_path)
                file_path = _build_artifact_test_folder(pytestconfig, request, file_name)
                video.save_as(path=file_path)
                # 放入视频
                allure.attach.file(file_path, name=f"{request.node.name}-{human_readable_status}-{index + 1}",
                                   attachment_type=allure.attachment_type.WEBM)
            except Error:
                # Silent catch empty videos.
                pass


#
# def _attach_test_artifacts(request, pytestconfig, pages, node_label):
#     """用例结束后统一处理：失败截图 + 视频，attach 到 Allure。
#     pages：本用例生命周期内创建过的所有 Page 对象列表（在页面关闭【前】调用）。"""
#     import shutil, os
#     from slugify import slugify
#     output_dir = pytestconfig.getoption("--output")
#     failed = getattr(request.node, "rep_call", None)
#     failed = failed.failed if failed else True
#     status = "failed" if failed else "finished"
#     base = os.path.join(output_dir, slugify(request.node.nodeid))
#
#     # ---- 1) 截图（page 还活着才能拍，所以必须在 close 之前调用本函数）----
#     if pytestconfig.getoption("--screenshot") == "on" or (
#         failed and pytestconfig.getoption("--screenshot") == "only-on-failure"):
#         for i, pg in enumerate(pages):
#             path = os.path.join(base, f"test-{status}-{i+1}.png")
#             try:
#                 pg.screenshot(timeout=5000, path=path)
#                 allure.attach.file(path, name=f"{node_label}-{status}-{i+1}",
#                                    attachment_type=allure.attachment_type.PNG)
#             except Error:
#                 pass
#
#     # ---- 2) 视频（同样在 close 前读取，避免关闭后访问 page.video 报错）----
#     if pytestconfig.getoption("--video") == "on" or (
#         failed and pytestconfig.getoption("--video") == "retain-on-failure"):
#         for i, pg in enumerate(pages):
#             video = pg.video
#             if not video:
#                 continue
#             src = video.path()
#             if not src or not os.path.exists(src):
#                 continue
#             dst = os.path.join(base, os.path.basename(src))
#             try:
#                 shutil.copy2(src, dst)
#                 allure.attach.file(dst, name=f"{node_label}-{i+1}",
#                                    attachment_type=allure.attachment_type.WEBM)
#             except Exception:
#                 pass
#
#
# @pytest.fixture(scope="session")
# def session_shared_context(browser: Browser, browser_context_args: dict, pytestconfig):
#     """
#     session全局共享BrowserContext，实现登录一次多条用例复用cookie
#     手动注入record_video_dir，解决session级别拿不到插件注入视频目录的问题
#     """
#     output_dir = pytestconfig.getoption("--output")
#     raw_video_dir = os.path.join(output_dir, "_session_raw_videos")
#     new_args = {**browser_context_args}
#     new_args["record_video_dir"] = raw_video_dir
#     ctx = browser.new_context(**new_args)
#     yield ctx
#     ctx.close()
#     # 会话结束删除原始视频缓存
#     import shutil
#     if os.path.exists(raw_video_dir):
#         shutil.rmtree(raw_video_dir)
#
#
# @pytest.fixture(scope="session")
# def login_prepare(session_shared_context: BrowserContext, base_url, pytestconfig):
#     """session内执行一次登录，cookie保存在session_shared_context内存中，不写磁盘文件"""
#     page = session_shared_context.new_page()
#     login_page = LoginPage(page)
#     login_page.navigate()
#     login_page.login("daij", "aa123456")
#     page.wait_for_url("**/index.html")
#     page.close()
#     yield
#
#
# @pytest.fixture
# def shared_page(session_shared_context, pytestconfig, request, login_prepare):
#     pages = []
#     session_shared_context.on("page", lambda pg: pages.append(pg))
#     p = session_shared_context.new_page()
#     yield p
#     _attach_test_artifacts(request, pytestconfig, pages, request.node.name)  # ★ close 之前
#     p.close()
#
# @pytest.fixture(scope="module")
# def unlogin_context(browser, base_url, pytestconfig, browser_context_args: Dict):
#     """
#     登录、注册页面（不依赖于先登录）单独创建独立的 context 上下文
#     避免全局先登录加载cookie，导致有些打开登录页直接跳到首页去了
#     :return:
#
#     1）browser
#     来源：pytest‑playwright 内置 fixture，session 级别，已经启动好的浏览器实例。
#     拿来干什么：调用 browser.new_context()，创建 BrowserContext 隔离环境。
#     2）base_url
#     pytest‑playwright 内置 fixture，没有使用，纯粹做依赖声明。
#     3）pytestconfig
#     pytest 内置 fixture，没有使用，向下游的unlogin_page做依赖链传递。
#     4）browser_context_args
#     来源：上面那个钩子 fixture 输出的配置字典。
#     拿来干什么：**browser_context_args 解包，传给 new_context，把窗口、证书的配置全部带进去。
#     """
#     context = browser.new_context(**browser_context_args)
#     yield context
#     context.close()
#
# @pytest.fixture
# def unlogin_page(unlogin_context, pytestconfig, request):
#     """
#     登录注册页面（不依赖于先登录）单独创建独立的 page 对象
#     带上用例失败截图和添加视频功能
#
#     1）unlogin_context
#     上一级 fixture unlogin_context yield 返回
#     隔离浏览器环境，执行 unlogin_context.new_page() 创建页面；同时绑定页面事件监听 .on("page")
#     2）pytestconfig
#     pytest 内置 fixture，截图时用上
#     读取命令行参数，调用工具函数等
#     3）request
#     pytest 内置 fixture
#     获取当前用例执行成功 / 失败，截图时用上
#     """
#     pages = []
#     unlogin_context.on("page", lambda pg: pages.append(pg))
#     p = unlogin_context.new_page()
#     yield p
#     _attach_test_artifacts(request, pytestconfig, pages, request.node.name)
#     p.close()


"""
    下面这个方案可以实现登录一次后保存上下文，
    然后加载到browser_context_args里面，
    但是因为现在版本内置的context是function级别的，
    每条用例执行一次都会销毁然后再生成，速度很慢
    所以放弃了这个方案
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

#
# @pytest.fixture(scope="session")
# def login_first(context, base_url, pytestconfig) -> None:
#     """有些网站网页关闭cookie就失效了，全局登录一次"""
#     # context = browser.new_context(base_url=base_url, no_viewport=True)
#     print("base_url----", base_url)
#     page = context.new_page()
#     LoginPage(page).navigate()
#     LoginPage(page).login("py", "123456")
#     # 等待登录成功页面重定向
#     page.wait_for_url(url='**/index.html')
