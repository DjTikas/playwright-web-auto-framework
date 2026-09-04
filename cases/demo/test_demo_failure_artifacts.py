import pytest
from playwright.sync_api import Page, expect

from cases.common.validation_data import ADD_PROJECT_FAILED_VALIDATION_CASES
from pages.add_project_page import AddProjectPage


class TestDemoFailureArtifacts:
    """失败截图/视频机制演示"""

    @pytest.fixture(autouse=True)
    def start_for_add_project(self, login_prepare,page: Page):
        print("for each--start: 打开新页面访问新增项目页")
        self.add_project = AddProjectPage(page)
        self.add_project.navigate()
        yield
        print("for each--end: 后置操作")

    @pytest.mark.parametrize('title, name, app, desc', ADD_PROJECT_FAILED_VALIDATION_CASES,
                             ids=[f"{t}" for t, _, _, _ in ADD_PROJECT_FAILED_VALIDATION_CASES])
    def test_add_project_validation(self, name, app, desc, title):
        """失败用例"""
        self.add_project.fill_project_name(name)
        self.add_project.fill_publish_app(app)
        self.add_project.fill_project_desc(desc)
        # 断言 按钮可点击
        expect(self.add_project.locator_submit_btn).to_be_enabled()