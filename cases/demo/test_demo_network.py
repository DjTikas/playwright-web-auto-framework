import pytest
from playwright.sync_api import Page


class TestDemoNetwork:
    """ajax 请求/响应断言、mock 原理演示"""

    @pytest.fixture(autouse=True)
    def start_for_login(self, unlogin_page: Page):
        print("for each--start: 打开新页面访问登录页")
        from pages.login_page import LoginPage
        self.login = LoginPage(unlogin_page)
        self.login.navigate()
        yield
        print("for each--end: 后置操作")

    @pytest.mark.demo('page.expect_ 显示断言')
    def test_login_success_expect(self):
        """成功登录，page.expect_ 显示断言"""
        self.login.fill_username('daij')
        self.login.fill_password('aa123456')
        with self.login.page.expect_navigation(url='**/index.html'):
            self.login.click_login_btn()

    @pytest.mark.demo('ajax请求')
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


    @pytest.mark.demo('ajax响应"')
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

