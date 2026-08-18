from playwright.sync_api import Page


class AddProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.locator_project_name = page.get_by_label('项目名称:')
        self.locator_publish_app = page.get_by_label('所属应用:')
        self.locator_project_desc = page.get_by_label('项目描述:')
        self.locator_submit_btn = page.get_by_role('button', name='点击提交')
        # 提示信息，忽略，因为和登录注册重复太多了
        # self.locator_project_name_tip1 = page.locator('[data-fv-validator="notEmpty"][data-fv-for="project_name"]')
        # 弹出的框，加 visible=True，只匹配显示出来的弹窗
        self.locator_bootbox = page.locator('.bootbox-body')

    def navigate(self):
        self.page.goto('/add_project.html')

    def fill_project_name(self, project_name):
        self.locator_project_name.fill(project_name)

    def fill_project_desc(self, project_desc):
        self.locator_project_desc.fill(project_desc)

    def fill_publish_app(self, publish_app):
        self.locator_publish_app.fill(publish_app)

    def click_submit_btn(self):
        self.locator_submit_btn.click()

    # 不知道拿来干嘛的
    def input_project(self, project_name: str, project_desc: str, publish_app: str) -> None:
        """
        新增项目
        :param name: 项目名称
        :param app: 发布app
        :param desc: 描述
        :return: None
        """
        self.locator_project_name.fill(project_name)
        self.locator_project_desc.fill(project_desc)
        self.locator_publish_app.fill(publish_app)
        # self.locator_submit_btn.click()