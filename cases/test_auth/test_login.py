import pytest
from playwright.sync_api import Page, expect
from cases.common.validation_data import FORM_VALIDATION_CASES
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
        # 每次重新导航会重置页面，登录按钮可以在输入框为空的情况下点击
        self.login.navigate()
        yield
        print("for each--end: 后置操作")

    @pytest.mark.parametrize("field, value, keyword", FORM_VALIDATION_CASES,
                             ids=[f"{f}-{k}" for f, _, k in FORM_VALIDATION_CASES])
    def test_form_validation(self, field, value, keyword):
        """登录页表单校验"""
        tip_text = self.login.fill_invalid_and_get_tip(field, value)
        assert tip_text is not None and keyword in tip_text
        expect(self.login.locator_login_btn).not_to_be_enabled()

    @pytest.mark.parametrize('username, pwd, title', [
        ['daij123', 'aa123456', '用户名错误，密码正确'],
        ['daij', 'aa123456789', '用户名正确，密码错误']
    ])
    def test_login_error(self, username:str, pwd: str, title:str):
        """用户名密码错误"""
        self.login.login(username, pwd)
        expect(self.login.locator_login_error).to_be_visible()

    def test_register_link(self):
        """点击跳转到注册页面"""
        # 先验证链接的属性
        expect(self.login.locator_register_link).to_have_attribute('href', 'register.html')
        self.login.locator_register_link.click()
        # 断言title和url
        expect(self.login.page).to_have_title('注册')
        expect(self.login.page).to_have_url('/register.html')

    def test_login_success_1(self):
        """成功登录，常规断言"""
        self.login.login('daij', 'aa123456')
        # 断言title和url
        expect(self.login.page).to_have_title('首页')
        expect(self.login.page).to_have_url('/index.html')

    @pytest.mark.skip('仅作为技术演示，不参与日常回归执行')
    def test_login_success_2(self):
        """成功登录，page.expect_ 显示断言"""
        self.login.fill_username('daij')
        self.login.fill_password('aa123456')
        with self.login.page.expect_navigation(url='**/index.html'):
            self.login.click_login_btn()

    @pytest.mark.skip('仅作为技术演示，不参与日常回归执行')
    def test_login_ajax_request(self):
        """正常登录，获取异步ajax请求"""
        self.login.fill_username('daij')
        self.login.fill_password('aa123456')
        # 捕获ajax请求，这里写的不是url，是接口路径
        with self.login.page.expect_request('**/api/login') as req:
            self.login.click_login_btn()
        # 获取请求对象
        print(req.value)
        # 断言请求内容
        assert req.value.method == 'POST'
        assert req.value.header_value('content-type') == 'application/json'
        assert req.value.post_data_json == {'username': 'daij', 'password': 'aa123456'}


    @pytest.mark.skip('仅作为技术演示，不参与日常回归执行')
    def test_login_ajax_response(self):
        """正常登录，获取异步ajax响应"""
        self.login.fill_username('daij')
        self.login.fill_password('aa123456')
        # 捕获ajax响应
        with self.login.page.expect_response('**/index.html') as res:
            self.login.click_login_btn()
        # 获取响应对象
        print(res.value)
        assert res.value.ok
        assert res.value.status == 200



"""       
    面试可以讲：
    “业务回归主要断言页面表现；
    同时我学习了 Playwright 网络事件监听，可以校验前端发出的请求报文、响应码，放在项目作为技术演示。”
"""