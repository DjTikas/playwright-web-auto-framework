import pytest
from playwright.sync_api import expect, Page

from mocks.mock_api import mock_project_400, mock_project_500, mock_project_200, mock_search_project_0, \
    mock_search_project_1, mock_project_delete_403, mock_project_render_10_row
from pages.project_list_page import ProjectListPage


class TestProjectList:
    """项目列表页"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, login_prepare, page: Page):
        print("for each--start: 打开项目列表页")
        self.project_list = ProjectListPage(page)
        self.project_list.navigate()
        yield
        print("for each--end: 后置操作")

    def test_project_list_render(self):
        """进入列表页，校验渲染正确"""
        self.project_list.page.route(**mock_project_render_10_row)
        self.project_list.navigate()

        # 等待loading消失（根据你项目实际类名调整）
        expect(self.project_list.page.locator(".loading")).to_be_hidden(timeout=3000)

        # ---------- 断言表头 th-inner 内文本 ----------
        ths = self.project_list.page.locator("thead.bg-info tr th .th-inner")
        # 0号：全选复选框那一列，没有可见文本，跳过文本断言，可以校验全选框可见
        expect(ths.nth(1)).to_have_text("ID")
        expect(ths.nth(2)).to_have_text("项目名称")
        expect(ths.nth(3)).to_have_text("所属应用")
        expect(ths.nth(4)).to_have_text("DebugTalk")
        expect(ths.nth(5)).to_have_text("测试人员")
        expect(ths.nth(6)).to_have_text("创建时间")
        # ⚠️重点：页面bug，update_time列展示文字依旧是“创建时间”，按页面实际结果断言
        expect(ths.nth(7)).to_have_text("创建时间")
        expect(ths.nth(8)).to_have_text("操作")

        # ---------- 断言tbody数据行数量 ----------
        table_data_rows = self.project_list.page.locator("tbody tr")
        expect(table_data_rows).to_have_count(10)


    def test_add_modal_open_dismiss(self):
        """新增项目，模态框取消"""
        self.project_list.click_add_project()
        # 断言模态框可见
        expect(self.project_list.locator_add_modal).to_be_visible()
        self.project_list.fill_add_project('aaa', '', '')
        self.project_list.dismiss_add_project()
        # 断言模态框隐藏
        expect(self.project_list.locator_add_modal).not_to_be_visible()

    def test_search_project_0(self):
        """项目列表搜索功能，mock搜索0个结果"""
        self.project_list.search_project_fill('test')
        # 期望输入框有内容
        expect(self.project_list.locator_search_box).to_have_value('test')
        # 点击搜素按钮
        self.project_list.page.route(**mock_search_project_0)
        self.project_list.click_search_btn()
        # 断言表列表内文本
        expect(self.project_list.locator_table_tr).to_contain_text('没有找到匹配的记录')

    def test_search_project_1(self):
        """项目列表搜索功能，mock搜索1个结果"""
        self.project_list.search_project_fill('test')
        # 期望输入框有内容
        expect(self.project_list.locator_search_box).to_have_value('test')
        # 点击搜素按钮
        self.project_list.page.route(**mock_search_project_1)
        self.project_list.click_search_btn()
        # 断言表列表包含一个值
        expect(self.project_list.locator_table_tr).to_have_count(1)

    def test_link(self):
        """表格行内的链接"""
        # 造数据，mock 行内数据
        self.project_list.page.route(**mock_search_project_1)
        # 刷新页面
        self.project_list.page.reload()
        # 断言链接的属性和指向
        # 这里的id必须要和mock里面的id一致
        expect(self.project_list.locator_table_link_debugtalk).to_have_attribute('href','debugtalk.html?project_id=1')

    def test_project_delete(self):
        """表格内删除项目。无法删除，需要管理员权限"""
        # 先造数据，mock 1条行内数据
        self.project_list.page.route(**mock_search_project_1)
        # 刷新页面
        self.project_list.page.reload()
        # 点击删除按钮
        self.project_list.locator_table_delete.click()
        # 弹出提示，mock拦截请求，点击确定删除
        expect(self.project_list.locator_bootbox).to_contain_text('确定要删除选中的数据？')
        self.project_list.page.route(**mock_project_delete_403)
        self.project_list.locator_bootbox_accept.click()
        # 有多个boot_box，获取最后一个
        expect(self.project_list.locator_bootbox.last).to_contain_text('操作异常："无权限操作，请联系管理员"')


    def test_project_edit(self):
        """表格行内编辑项目"""
        # 注意，表格同一行中有两个地方，鼠标悬浮时都会出现“编辑”，两处点击效果是一样的
        # 所以，要加上first，定位其中一个
        self.project_list.locator_table_edit.first.click()
        # 断言模态框出现
        expect(self.project_list.locator_edit_modal).to_be_visible()
        self.project_list.locator_edit_app.fill('test2026')
        self.project_list.locator_edit_save_btn.click()
        # -------------------------- 保存后断言闭环 --------------------------
        # 1. 编辑模态框关闭消失
        expect(self.project_list.locator_edit_modal).to_be_hidden(timeout=5000)
        # 表格tbody第一行，所属应用那一列 td，校验文本变成新值
        # 先定位第一行tr，再定位该行下的所属应用单元格（对应表头data‑field="publish_app"那一列）
        first_row = self.project_list.page.locator("tbody tr").first
        # 所属应用是第3个td，索引从0开始：0复选框，1ID，2项目名称，3所属应用
        expect(first_row.locator("td").nth(3)).to_have_text('test2026')
