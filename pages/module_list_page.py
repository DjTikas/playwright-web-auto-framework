from playwright.sync_api import Page, expect


class ModuleListPage:
    """模块列表"""
    def __init__(self, page: Page):
        self.page = page
        self.locator_add_module_btn = page.get_by_role('button', name='新增模块')
        self.locator_search_module_box = page.get_by_placeholder('模块名称')
        self.locator_refresh_btn = page.get_by_title('刷新')
        self.locator_search_btn = page.get_by_role('button', name='搜索')
        # 下拉框定位
        self.locator_project_selector_btn = page.get_by_role('button', name='选择项目')
        self.locator_project_list_box = page.get_by_role('listbox')
        # 新增模块模态框
        self.locator_add_modal = page.locator('#addModal')
        self.locator_add_modal_name = self.locator_add_modal.get_by_label('模块名称')
        self.locator_add_modal_project = self.locator_add_modal.get_by_label('所属项目')
        self.locator_add_modal_desc = self.locator_add_modal.get_by_label('模块描述')
        self.locator_add_modal_save_btn = self.locator_add_modal.get_by_role('button', name='保存')
        self.locator_add_modal_desc = self.locator_add_modal.get_by_role('button', name='取消')
        # 编辑模块模态框
        self.locator_edit_modal = page.locator('#myModal')
        # 表格
        self.locator_table_tr = page.locator('//tbody/tr')
        self.locator_edit_btn = self.locator_table_tr.get_by_title('编辑').first
        self.locator_delete_btn = self.locator_table_tr.get_by_title('删除')
        # bootbox-body
        self.locator_bootbox_body = page.locator('.bootbox-body')
        # 下一页
        # ModuleListPage类内定位器
        self.locator_pag_next = page.locator(".fixed-table-pagination .page-next a")
        # 分页‑每页条数下拉按钮
        self.locator_pagesize_dropdown_btn = page.locator(".page-list .btn.dropdown-toggle")
        # 下拉菜单选项，根据文本匹配
        self.locator_pagesize_menu_item = page.locator(".page-list .dropdown-menu li a")

    def navigate(self):
        self.page.goto('list_module.html')

    def fill_search_box(self, name):
        self.locator_search_module_box.fill(name)

    def select_project_by_value(self, value):
        self.locator_project_selector_btn.click()
        expect(self.locator_project_list_box).to_be_visible()
        self.locator_project_list_box.get_by_role('option', name=value).click()

    def click_add_modal_btn(self):
        self.locator_add_modal.click()

    def switch_page_size(self, text: str):
        """
        切换每页条数
        text: "10" / "15" / "20" / "50" / "所有"
        """
        # 点开下拉
        self.locator_pagesize_dropdown_btn.click()
        # 点击对应文本的选项
        self.locator_pagesize_menu_item.get_by_text(text, exact=True).click()

