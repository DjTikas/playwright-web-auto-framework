import allure
from playwright.sync_api import Page

class RegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.locator_username = page.get_by_label("用 户 名:")
        self.locator_password = page.get_by_label("密     码:")
        self.locator_register_btn = page.get_by_role("button", name="立即注册 > ")
        self.locator_login_link = page.get_by_text("已有账号？点这登录")
        # 用户名输入框提示语
        self.locator_username_tip1 = page.locator('[data-fv-validator="notEmpty"][data-fv-for="username"]')
        self.locator_username_tip2 = page.locator('[data-fv-validator="stringLength"][data-fv-for="username"]')
        self.locator_username_tip3 = page.locator('[data-fv-validator="regexp"][data-fv-for="username"]')
        # 密码输入框提示语
        self.locator_password_tip1 = page.locator('[data-fv-validator="notEmpty"][data-fv-for="password"]')
        self.locator_password_tip2 = page.locator('[data-fv-validator="stringLength"][data-fv-for="password"]')
        self.locator_password_tip3 = page.locator('[data-fv-validator="regexp"][data-fv-for="password"]')
        # 提示用户已存在
        self.locator_register_error = page.get_by_text('用户名已存在或不合法！')

    def navigate(self):
        with allure.step("导航到注册页"):
            self.page.goto('/register.html')

    def fill_username(self, username):
        with allure.step(f"输入用户名{username}"):
            self.locator_username.fill(username)

    def fill_password(self, password):
        with allure.step(f"输入用密码{password}"):
            self.locator_password.fill(password)

    def click_register_btn(self):
        with allure.step("点击注册按钮"):
            self.locator_register_btn.click()

    def click_login_link(self):
        with allure.step("点击登录链接"):
            self.locator_login_link.click()

    def register(self, username, password):
        with allure.step(f"输入用户名{username}，密码{password}，点击登录"):
            self.fill_username(username)
            self.fill_password(password)
            self.click_register_btn()