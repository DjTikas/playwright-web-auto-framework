import uuid
import pytest
from playwright.sync_api import Page, expect
from cases.common.validation_data import FORM_VALIDATION_CASES
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

    @pytest.mark.parametrize("field, value, keyword", FORM_VALIDATION_CASES,
                             ids=[f"{f}-{k}" for f, _, k in FORM_VALIDATION_CASES])
    def test_form_validation(self, field, value, keyword):
        """注册页表单校验"""
        tip_text = self.register.fill_invalid_and_get_tip(field, value)
        assert tip_text is not None and keyword in tip_text
        expect(self.register.locator_register_btn).not_to_be_enabled()

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