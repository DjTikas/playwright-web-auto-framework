from playwright.sync_api import Page


class AddModulePage:
    """新增模块页面"""
    def __init__(self, page: Page):
        self.page = page
        self.locator_module_name = page.get_by_label('模块名称:')
        self.locator_module_project = page.get_by_label('所属项目')
        self.locator_module_desc = page.get_by_label('模块描述:')
        self.locator_submit_btn = page.get_by_role('button', name='点击提交')
        # 模态框
        self.locator_bootbox_body = page.locator('.bootbox-body')


    def navigate(self):
        self.page.goto('/add_module.html')

    def fill_module_name(self, name):
        self.locator_module_name.fill(name)

    def fill_module_desc(self, desc):
        self.locator_module_desc.fill(desc)

    def select_project_by_value(self, value):
        self.locator_module_project.select_option(value=value)

    def click_submit_btn(self):
        self.locator_submit_btn.click()