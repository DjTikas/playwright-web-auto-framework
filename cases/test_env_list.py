import pytest
from playwright.sync_api import Page, expect

from cases.common.validation_data import ADD_ENV_VALIDATION_CASES
from mocks.mock_api import mock_add_env_400, mock_add_env_201
from pages.env_list_page import EnvListPage


class TestEnvList:
    """环境列表页面"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, login_prepare, page: Page):
        print("for each--start: 打开环境列表页")
        self.env = EnvListPage(page)
        self.env.navigate()
        yield
        print("for each--end: 后置操作")

    @pytest.mark.parametrize("title, name, address, keyword", ADD_ENV_VALIDATION_CASES,
                             ids=(f"{t}" for t, _, _, _ in ADD_ENV_VALIDATION_CASES))
    def test_env_name_validation(self, title, name, address, keyword):
        """新增环境：表单校验"""
        self.env.click_add_env()  # 弹出新增框
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        tip_text = self.env.fill_invalid_and_get_tip(title, name, address)
        assert tip_text is not None and keyword in tip_text


    @pytest.mark.parametrize("address", ["abchttp", "httpx:", "httpsx://"])
    def test_add_env_address_invalid(self, address):
        """新增环境：环境地址必须以http:或 https:开头"""
        self.env.click_add_env()  # 弹出新增框
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.input_env_name('env')
        self.env.input_env_address(address)
        self.env.click_modal_save()
        # 断言不能为空
        expect(self.env.locator_boot_box).to_be_visible()
        expect(self.env.locator_boot_box).to_have_text('操作异常：{"base_url":"base_url must start with http:// or https://"}')

    def test_add_env_dismiss(self):
        """新增环境：点取消按钮"""
        self.env.click_add_env()  # 弹出新增框
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.input_env_name('')
        self.env.click_modal_dismiss()  # 取消按钮
        # 断言模态框不显示
        expect(self.env.locator_add_modal).not_to_be_visible()

    def test_add_env_exists_400(self):
        """新增环境：环境名称已存在"""
        self.env.click_add_env()  # 弹出新增框
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.input_env_name('test123')
        self.env.input_env_address('http://www.yoyo.com')
        # mock 返回400 已存在
        self.env.page.route(**mock_add_env_400)
        self.env.click_modal_save()
        # 断言已存在
        expect(self.env.locator_boot_box).to_be_visible()
        expect(self.env.locator_boot_box).to_have_text('操作异常：{"env_name":"env_name: test123 已存在"}')

    def test_add_env_success_201(self):
        """新增环境：环境新增成功"""
        self.env.click_add_env()  # 弹出新增框
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.input_env_name('test2026')
        self.env.input_env_address('http://www.baidu.com')
        # mock 返回201 成功
        self.env.page.route(**mock_add_env_201)
        # with self.env.page.expect_request('**/api/env')
        self.env.click_modal_save()
        # 断言添加成功
        expect(self.env.locator_add_modal).to_be_hidden()