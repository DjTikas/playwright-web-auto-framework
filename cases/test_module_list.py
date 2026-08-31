import pytest
from playwright.sync_api import expect

from mocks.mock_api import mock_project_select_200, mock_module_list_table_page_1, mock_module_list_table_page_2, \
    mock_module_list_table_10_row
from pages.module_list_page import ModuleListPage


class TestModuleList:
    """模块列表页"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, login_prepare, shared_page):
        print('for each--start：打开模块列表页面')
        self.module_list = ModuleListPage(shared_page)
        self.module_list.page.route(**mock_project_select_200)
        self.module_list.page.route(**mock_module_list_table_page_1)
        self.module_list.navigate()
        yield
        print('for each--end：后置操作')

    def test_table_render_correct(self):
        """表格渲染校验"""
        # 断言 表格行数、文本内容
        expect(self.module_list.locator_table_tr).to_have_count(15)
        expect(self.module_list.locator_table_tr.first).to_contain_text('123aaa')

    def test_pagination_switch_page(self):
        """切换到第 2 页，校验请求参数和页面数据"""
        self.module_list.page.route(**mock_module_list_table_page_2)
        with self.module_list.page.expect_request('**/api/module**') as req:
            self.module_list.locator_pag_next.click()
        # 断言请求参数
        assert 'page=2' in req.value.url
        assert 'size=15' in req.value.url
        assert req.value.method == 'GET'
        # 断言页面渲染第二页数据
        expect(self.module_list.locator_table_tr).to_have_count(10)
        expect(self.module_list.locator_table_tr.first).to_contain_text("108aaa")

        self.module_list.locator_pag_next.click()

    def test_pagination_change_page_size(self):
        """分页修改每页条数（15→10），校验接口请求参数"""
        self.module_list.page.route(**mock_module_list_table_10_row)
        with self.module_list.page.expect_request('**/api/module**') as req:
            self.module_list.switch_page_size('10')
        assert req.value.method == 'GET'
        assert 'size=10' in req.value.url
        expect(self.module_list.locator_table_tr).to_have_count(10)

    def test_search_refresh_btn(self):
        """测试重置按钮"""
        self.module_list.page.route(**mock_module_list_table_page_2)
        self.module_list.locator_pag_next.click()
        with self.module_list.page.expect_request('**/api/module**') as req:
            self.module_list.locator_refresh_btn.click()
        assert 'page=1' in req.value.url
        assert 'size=15' in req.value.url
        assert req.value.method == 'GET'

    def test_search_combine_project_select(self):
        """组合条件查询：项目下拉框 + 模块名称关键词同时筛选"""
        self.module_list.select_project_by_value('test_module')
        self.module_list.locator_search_module_box.fill('123aaa')
        with self.module_list.page.expect_request('**/api/module**') as req:
            self.module_list.locator_search_btn.click()
        assert 'module_name=123aaa' in req.value.url
        # 这里test_module对应的id是1111
        assert 'project=1111' in req.value.url
        assert req.value.method == 'GET'