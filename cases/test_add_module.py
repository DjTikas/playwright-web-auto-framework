import pytest
from playwright.sync_api import expect

from mocks.mock_api import mock_project_select_200, mock_module_repeat_400, mock_add_module_201
from pages.add_module_page import AddModulePage


class TestAddModule:
    """新增模块页面"""
    @pytest.fixture(autouse=True)
    def start_for_each(self, login_prepare, shared_page):
        print('for each--start：打开新增模块页面')
        self.add_module = AddModulePage(shared_page)
        # 拦截项目选项数据，模拟返回选项
        self.add_module.page.route(**mock_project_select_200)
        self.add_module.navigate()
        yield
        print('for each--end：后置操作')

    def test_add_module_name_null(self):
        """模块名为空"""
        self.add_module.fill_module_name('')
        self.add_module.click_submit_btn()
        # 断言按钮不可点击
        expect(self.add_module.locator_submit_btn).to_be_disabled()

    def test_add_module_project_null(self):
        """项目名为空"""
        self.add_module.fill_module_name('test')
        self.add_module.click_submit_btn()
        # 断言按钮不可点击
        expect(self.add_module.locator_submit_btn).to_be_disabled()

    def test_add_module_repeat(self):
        """模块名重复"""
        self.add_module.fill_module_name('test')
        self.add_module.select_project_by_value('test')
        # mock 400数据
        self.add_module.page.route(**mock_module_repeat_400)
        self.add_module.click_submit_btn()
        # 断言提示框内容
        expect(self.add_module.locator_bootbox_body).to_be_visible()
        expect(self.add_module.locator_bootbox_body).to_contain_text('已存在')

    def test_add_module_success(self):
        """添加模块成功"""
        self.add_module.fill_module_name('testxx')
        self.add_module.select_project_by_value('test')
        self.add_module.fill_module_desc('xxx')
        # mock 201数据
        self.add_module.page.route(**mock_add_module_201)
        self.add_module.click_submit_btn()
        # 断言跳转页面
        expect(self.add_module.page).to_have_title('模块列表')
        expect(self.add_module.page).to_have_url('/list_module.html')

