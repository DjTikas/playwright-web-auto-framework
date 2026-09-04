import uuid

import pytest
from playwright.sync_api import Page, expect

from cases.common.validation_data import ADD_PROJECT_VALIDATION_CASES
from mocks import mock_api
from pages.add_project_page import AddProjectPage


class TestAddProject:
    """新增项目页"""
    @pytest.fixture(autouse=True)
    def start_for_each(self, login_prepare, page: Page):
        print("for each--start: 打开添加项目页")
        self.add_project = AddProjectPage(page)
        self.add_project.navigate()
        yield
        print("for each--end: 后置操作")

    def test_add_project_success(self):
        """添加成功，判断项目列表页面中存在新增的项目"""
        project_name = str(uuid.uuid4())[:8]
        self.add_project.fill_project_name(project_name)
        self.add_project.click_submit_btn()
        # 断言跳项目列表 title/url
        expect(self.add_project.page).to_have_title('项目列表')
        expect(self.add_project.page).to_have_url('/list_project.html')
        # 点击保存后等页面重定向到table表格页
        self.add_project.page.wait_for_load_state('networkidle')
        # 等待表格DOM出现，再去all拿元素，减少偶发空列表
        self.add_project.page.locator("#table").wait_for()
        # 断言新增项目在列表页
        # 获取页面 table 表格-项目名称列全部内容
        locator_projects = self.add_project.page.locator(
            '//table[@id="table"]//td[3]/a'
        )
        project_name_list = [i.inner_text() for i in locator_projects.all()]
        assert project_name in project_name_list

    @pytest.mark.parametrize('title, name, app, desc', ADD_PROJECT_VALIDATION_CASES,
                             ids=[f"{t}" for t, _, _, _ in ADD_PROJECT_VALIDATION_CASES])
    def test_add_project_validation(self, name, app, desc, title):
        """信息填写校验"""
        self.add_project.fill_project_name(name)
        self.add_project.fill_publish_app(app)
        self.add_project.fill_project_desc(desc)
        if title == '项目名称为空':
            self.add_project.click_submit_btn()
        # 断言 按钮不可点击
        expect(self.add_project.locator_submit_btn).to_be_disabled()

    def test_add_project_repeat_400(self):
        """项目已存在，弹出模态框，400状态码"""
        self.add_project.fill_project_name('test')
        # mock 接口返回400
        self.add_project.page.route(**mock_api.mock_project_400)
        self.add_project.click_submit_btn()
        # 校验结果 弹出框文本包含
        expect(self.add_project.locator_bootbox).to_be_visible()
        expect(self.add_project.locator_bootbox).to_contain_text('已存在')

    def test_add_project_server_500(self):
        """服务器异常，500状态码"""
        self.add_project.fill_project_name('test')
        # mock 接口返回500
        self.add_project.page.route(**mock_api.mock_project_500)
        self.add_project.click_submit_btn()
        # 校验结果 弹出框文本包含
        expect(self.add_project.locator_bootbox).to_be_visible()
        expect(self.add_project.locator_bootbox).to_contain_text('操作异常')

