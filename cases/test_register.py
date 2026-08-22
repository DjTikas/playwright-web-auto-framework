import uuid

import pytest
from playwright.sync_api import Page, expect
from pages.register_page import RegisterPage


class TestRegister:
    """注册功能"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, unlogin_page: Page):
        """
        注册功能用独立的上下文环境，不加载cookie
        :param unlogin_page: 独立上下文
        :return: None
        """
        print("for each--start: 打开新页面访问注册页")
        self.register = RegisterPage(unlogin_page)
        self.register.navigate()
        yield
        print('后置操作')

    def test_register_1(self):
        """用户名为空，点注册"""
        self.register.fill_username('')
        self.register.fill_password('123456aa')
        self.register.click_register_btn()
        # 断言
        expect(self.register.locator_username_tip1).to_be_visible()
        expect(self.register.locator_username_tip1).to_contain_text('不能为空')

    def test_register_2(self):
        """用户名超过30位"""
        self.register.fill_username('123456789012345678901234567890123456')
        self.register.fill_password('123456aa')
        # 断言
        expect(self.register.locator_username_tip2).to_be_visible()
        expect(self.register.locator_username_tip2).to_contain_text('用户名称1-30位字符')
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_register_3(self):
        """用户名包含特殊字符"""
        self.register.fill_username('daij')
        self.register.fill_password('123456aa')
        # 断言
        expect(self.register.locator_username_tip3).to_be_visible()
        expect(self.register.locator_username_tip3).to_contain_text('用户名称不能有特殊字符,请用中英文数字_')
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_register_4(self):
        """密码为空，点登录"""
        self.register.fill_username('daij')
        self.register.fill_password('')
        self.register.click_register_btn()
        # 断言
        expect(self.register.locator_password_tip1).to_be_visible()
        expect(self.register.locator_password_tip1).to_contain_text('不能为空')

    # 不知道为什么加上了title，估计是allure报告会用上吧
    @pytest.mark.parametrize('username, pwd, title', [
        ['tikas', '12345678901234567890', '密码超过16位'],
        ['daij', '123', '密码少于6位'],
    ])
    def test_register_5(self, username:str, pwd: str, title:str):
        """密码小于6位或者大于16位"""
        self.register.fill_username(username)
        self.register.fill_password(pwd)
        # 断言
        expect(self.register.locator_password_tip2).to_be_visible()
        expect(self.register.locator_password_tip2).to_contain_text('密码6-16位字符')
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_register_6(self):
        """密码包含特殊字符"""
        self.register.fill_username('daij')
        self.register.fill_password('123456aa*-')
        # 断言
        expect(self.register.locator_password_tip3).to_be_visible()
        expect(self.register.locator_password_tip3).to_contain_text('不能有特殊字符,请用中英文数字下划线')
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_register_7(self):
        """用户名密码同时为空"""
        self.register.fill_username('')
        self.register.fill_password('')
        self.register.click_register_btn()
        # 断言
        expect(self.register.locator_username_tip1).to_be_visible()
        expect(self.register.locator_username_tip1).to_contain_text('不能为空')
        expect(self.register.locator_password_tip1).to_be_visible()
        expect(self.register.locator_password_tip1).to_contain_text('不能为空')

    def test_register_error(self):
        """用户名已存在"""
        self.register.register('daij', 'aa123456')
        expect(self.register.locator_register_error).to_be_visible()

    def test_login_link(self):
        """点击跳转到登录页面"""
        expect(self.register.locator_login_link).to_have_attribute('href', 'login.html')
        self.register.click_login_link()
        expect(self.register.page).to_have_title('网站登录')
        expect(self.register.page).to_have_url('/login.html')

    def test_register_success(self):
        """注册新账号成功"""
        username = str(uuid.uuid4())[:8]
        pwd = 'aa123456'
        self.register.register(username, pwd)
        expect(self.register.page).to_have_title('首页')
        expect(self.register.page).to_have_url('/index.html')