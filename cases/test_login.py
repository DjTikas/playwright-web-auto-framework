import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


class TestLogin:
    """登录功能"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, unlogin_page: Page):
        """
        登录功能用独立的上下文环境，不加载cookie
        :param unlogin_page: 独立上下文
        :return: None
        """
        print("for each--start: 打开新页面访问登录页")
        self.login = LoginPage(unlogin_page)
        self.login.navigate()
        yield
        print("for each--end: 后置操作")

    def test_login_1(self):
        """用户名为空，点登录"""
        self.login.fill_username('')
        self.login.fill_password('123456aa')
        self.login.click_login_btn()
        # 断言
        expect(self.login.locator_username_tip1).to_be_visible()
        expect(self.login.locator_username_tip1).to_contain_text('不能为空')

    def test_login_2(self):
        """用户名超过30位"""
        self.login.fill_username('123456789012345678901234567890123456')
        self.login.fill_password('123456aa')
        # 断言
        expect(self.login.locator_username_tip2).to_be_visible()
        expect(self.login.locator_username_tip2).to_contain_text('用户名称1-30位字符')
        expect(self.login.locator_login_btn).not_to_be_enabled()

    def test_login_3(self):
        """用户名包含特殊字符"""
        self.login.fill_username('daij*@')
        self.login.fill_password('123456aa')
        # 断言
        expect(self.login.locator_username_tip3).to_be_visible()
        expect(self.login.locator_username_tip3).to_contain_text('用户名称不能有特殊字符,请用中英文数字_')
        expect(self.login.locator_login_btn).not_to_be_enabled()

    def test_login_error(self):
        """用户名密码错误"""
        self.login.login('daij', '123456aa')
        expect(self.login.locator_login_error).to_be_visible()
