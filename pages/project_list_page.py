from playwright.sync_api import Page


class ProjectListPage:

    def __init__(self, page: Page):
        self.page = page
        self.locator_btn_add = page.get_by_role('button', name='新增项目')
        self.locator_search_box = page.get_by_placeholder('项目名称')
        self.locator_btn_search = page.get_by_role('button', name='搜索')
        # 新增项目模态框
        self.locator_add_modal = page.locator('#addModal')
        self.locator_modal_project_name = self.locator_add_modal.get_by_label('项目名称:')
        self.locator_modal_publish_app = self.locator_add_modal.get_by_label('所属应用:')
        self.locator_modal_project_desc = self.locator_add_modal.get_by_label('项目描述:')
        self.locator_modal_btn_save = self.locator_add_modal.get_by_text('保存')
        self.locator_modal_btn_dismiss = self.locator_add_modal.get_by_text('取消')
        # 编辑项目模态框
        self.locator_edit_modal = page.locator('#myModal')
        self.locator_edit_app = self.locator_edit_modal.locator('#publish_app')
        self.locator_edit_save_btn = self.locator_edit_modal.get_by_role('button', name='保存')
        # 刷新页面按钮
        self.locator_refresh = page.get_by_title('刷新')
        # table表格按钮
        self.locator_table_tr = page.locator('//tbody/tr')
        self.locator_table_edit = self.locator_table_tr.get_by_title('编辑')
        self.locator_table_delete = self.locator_table_tr.get_by_title('删除')
        self.locator_table_link_debugtalk = self.locator_table_tr.get_by_text('debugtalk.py')
        # bootbox-body
        self.locator_bootbox = page.locator('.bootbox-body')
        self.locator_bootbox_accept = page.get_by_text('确定删除')
        self.locator_bootbox_dismiss = page.get_by_text('取消操作')

    def navigate(self):
        self.page.goto('/list_project.html')

    def click_add_project(self):
        self.locator_btn_add.click()

    def fill_add_project(self, name, app, desc):
        self.locator_modal_project_name.fill(name)
        self.locator_modal_project_desc.fill(desc)
        self.locator_modal_publish_app.fill(app)

    def click_save_add_project(self):
        self.locator_modal_btn_save.click()

    def dismiss_add_project(self):
        self.locator_modal_btn_dismiss.click()

    def search_project_fill(self, name):
        self.locator_search_box.fill(name)

    def click_search_btn(self):
        self.locator_btn_search.click()

    def click_refresh(self):
        self.locator_refresh.click()