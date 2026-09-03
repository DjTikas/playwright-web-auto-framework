from typing import Optional

from playwright.sync_api import Page


class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.locator_username = page.get_by_label("用 户 名:")
        self.locator_password = page.get_by_label("密     码:")
        self.locator_login_btn = page.get_by_role("button", name="立即登录 > ")
        self.locator_register_link = page.get_by_text("没有账号？点这注册")
        # 用户名输入框提示语
        self.locator_username_tip1 = page.locator('[data-fv-validator="notEmpty"][data-fv-for="username"]')
        self.locator_username_tip2 = page.locator('[data-fv-validator="stringLength"][data-fv-for="username"]')
        self.locator_username_tip3 = page.locator('[data-fv-validator="regexp"][data-fv-for="username"]')
        # 密码输入框提示语
        self.locator_password_tip1 = page.locator('[data-fv-validator="notEmpty"][data-fv-for="password"]')
        self.locator_password_tip2 = page.locator('[data-fv-validator="stringLength"][data-fv-for="password"]')
        self.locator_password_tip3 = page.locator('[data-fv-validator="regexp"][data-fv-for="password"]')
        # 账号或密码不正确！
        self.locator_login_error = page.locator('text=账号或密码不正确！')

    def navigate(self):
        """导航到登录页面"""
        self.page.goto('/login.html')

    def fill_username(self, username):
        """输入用户名"""
        self.locator_username.fill(username)

    def fill_password(self, password):
        """输入密码"""
        self.locator_password.fill(password)

    def click_login_btn(self):
        """点击登录按钮"""
        self.locator_login_btn.click()

    def click_register_link(self):
        """点击跳转注册页面"""
        self.locator_register_link.click()

    def login(self, username, password):
        """完整登录操作"""
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_btn()

    def fill_invalid_and_get_tip(self, field: str, value: str) -> Optional[str]:
        """填入非法值，返回当前可见的字段提示文本；无提示返回 None"""
        if field == "username":
            self.fill_username(value)
            self.fill_password("123456aa")  # 让用户名单独触发校验
            if value == '':
                self.locator_login_btn.click()
            tips = [self.locator_username_tip1, self.locator_username_tip2, self.locator_username_tip3]
        else:
            self.fill_username("daij")
            self.fill_password(value)  # 让密码单独触发校验
            if value == '':
                self.locator_login_btn.click()
            tips = [self.locator_password_tip1, self.locator_password_tip2, self.locator_password_tip3]
        for tip in tips:
            if tip.is_visible():
                return tip.inner_text()
        return None
