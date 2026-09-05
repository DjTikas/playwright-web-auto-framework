import os
import shutil
from pytest import Item
import allure
import pytest
from typing import Dict

# 本地插件注册
pytest_plugins = ['plugins.pytest_playwright']

# ========== 定义浏览器前缀（用于截断） ==========
BROWSER_PREFIXES = ['chromium-', 'firefox-', 'webkit-', 'msedge-']

def decode_unicode_escape(s: str) -> str:
    try:
        if '\\u' in s:
            return s.encode('utf-8').decode('unicode_escape')
        return s
    except Exception:
        return s

def pytest_runtest_call(item: Item):
    if item.parent and item.parent._obj.__doc__:
        allure.dynamic.feature(item.parent._obj.__doc__.strip())

    base_title = item.function.__doc__.strip() if item.function.__doc__ else item.name

    if hasattr(item, 'callspec') and item.callspec.id:
        full_id = item.callspec.id
        # 去掉浏览器前缀
        custom_id = full_id
        for prefix in BROWSER_PREFIXES:
            if full_id.startswith(prefix):
                custom_id = full_id[len(prefix):]
                break
        # 转码
        custom_id = decode_unicode_escape(custom_id)

        if custom_id:
            title = f"{base_title} - {custom_id}"
        else:
            title = base_title
    else:
        title = base_title

    allure.dynamic.title(title)


def _clean_dir(dir_path: str):
    """清理allure相关目录"""
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


# 重写插件钩子 1
# 生产参数字典，供给 pytest‑playwright 内部，用于启动浏览器。
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args) -> Dict:
    """窗口最大化"""
    return {"args": ['--start-maximized'], **browser_type_launch_args}


# 重写插件钩子 2
# 生产参数字典，输出一个配置字典。
# unlogin_context等固件会 消费这个字典
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright, pytestconfig) -> Dict:
    """窗口最大化"""
    return {
        "no_viewport": True,
        # 忽略https报错
        "ignore_https_errors": True,
        **browser_context_args
    }



from dingtalkchatbot.chatbot import DingtalkChatbot
import time
def ding_ding_notify(
    access_token, secret=None, pc_slide=False, fail_notice=False,
    title="测试报告", text="## 测试报告", is_at_all=False,
    at_mobiles=None, at_dingtalk_ids=None, is_auto_at=True, *args, **kwargs): # noqa
    """
    机器人初始化
    :param access_token: 钉钉群自定义机器人access_token
    :param secret: 机器人安全设置页面勾选"加签"时需要传入的密钥
    :param pc_slide: 消息链接打开方式，默认False为浏览器打开，设置为True时为PC端侧边栏打开
    :param fail_notice: 消息发送失败提醒，默认为False不提醒，开发者可以根据返回的消息发送结
    果自行判断
    钉钉机器人通知报告
    markdown类型
    :param title: 首屏会话透出的展示内容
    :param text: markdown格式的消息内容
    :param is_at_all: @所有人时：true，否则为：false（可选）
    :param at_mobiles: 被@人的手机号
    :param at_dingtalk_ids: 被@用户的UserId（企业内部机器人可用，可选）
    :param is_auto_at: 是否自动在text内容末尾添加@手机号，默认自动添加，也可设置为False，然后自行在
    :return: 返回消息发送结果
    """
    webhook = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
    ding = DingtalkChatbot(webhook=webhook, secret=secret, pc_slide=pc_slide, fail_notice=fail_notice)
    ding.send_markdown(
        title=title, text=text, is_at_all=is_at_all,
        at_mobiles=at_mobiles if at_mobiles else [],
        at_dingtalk_ids=at_dingtalk_ids if at_dingtalk_ids else [],
        is_auto_at=is_auto_at
    )

# 修改配置
DING_TALK = {
    "access_token": "dd718e6c7c71da6248a2c7e7442afe9aa0ad0719983f984b2f1ac8b4a764c1fb",
    "title": "测试报告",
    "at_mobiles": ["15719497316", '183********'],
    "text": "- 查看报告：[allure报告地址](http://106.55.15.17:8082/index.html)"
}

def pytest_terminal_summary(terminalreporter, exitstatus, config): # noqa
    """收集测试结果"""
    base_url = config.getoption("--base-url") or config.getini("base_url")
    print(f"------------{base_url}")
    total = terminalreporter._numcollected # noqa
    if total > 0:
        passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
        failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
        error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
        # skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
        successful = len(terminalreporter.stats.get('passed', [])) / terminalreporter._numcollected
        duration = time.time()- terminalreporter._sessionstarttime # noqa
        markdown_text = f"""### 执行结果:
- 运行环境: 测试环境
- 运行base_url: {base_url}
- 持续时间: {duration: .2f} 秒

### 本次运行结果:
- 总用例数: {total}
- 通过用例：{passed}
- 失败用例： {failed}
- 异常用例： {error}
- 通过率： {successful: .2f} % \n
"""
        if DING_TALK.get('text'):
            DING_TALK['text'] = markdown_text + DING_TALK['text']
        else:
            DING_TALK['text'] = markdown_text
        ding_ding_notify(**DING_TALK)