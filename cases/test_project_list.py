import pytest
from playwright.sync_api import expect

from mocks.mock_api import mock_project_400, mock_project_500, mock_project_200, mock_search_project_0, \
    mock_search_project_1, mock_project_delete_403
from pages.project_list_page import ProjectListPage


class TestProjectList:
    """项目列表页"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, login_prepare, shared_page):
        print("for each--start: 打开项目列表页")
        self.project_list = ProjectListPage(shared_page)
        self.project_list.navigate()
        yield
        print("for each--end: 后置操作")

    @pytest.mark.skip('同类型的用例比较多')
    def test_add_project_null(self):
        """新增项目，项目名为空"""
        self.project_list.click_add_project()
        self.project_list.fill_add_project('', '', '')
        self.project_list.click_save_add_project()
        # 断言模态框不隐藏
        expect(self.project_list.locator_add_modal).not_to_be_hidden()

    @pytest.mark.skip('同类型的用例比较多')
    def test_add_project_dismiss(self):
        """新增项目，模态框取消"""
        self.project_list.click_add_project()
        self.project_list.fill_add_project('aaa', '', '')
        self.project_list.dismiss_add_project()
        # 断言模态框隐藏
        expect(self.project_list.locator_add_modal).not_to_be_visible()

    def test_add_project_400(self):
        """新增已有项目，状态码400"""
        self.project_list.click_add_project()
        self.project_list.fill_add_project('aaa', '', '')
        self.project_list.page.route(**mock_project_400)
        self.project_list.click_save_add_project()
        # 断言bootbox
        expect(self.project_list.locator_bootbox).to_be_visible()
        expect(self.project_list.locator_bootbox).to_contain_text('已存在')

    def test_add_project_500(self):
        """新增项目，服务器错误500"""
        self.project_list.click_add_project()
        self.project_list.fill_add_project('aaa', '', '')
        self.project_list.page.route(**mock_project_500)
        self.project_list.click_save_add_project()
        # 断言bootbox
        expect(self.project_list.locator_bootbox).to_be_visible()
        expect(self.project_list.locator_bootbox).to_contain_text('操作异常')

    def test_add_project_200(self):
        """新增项目成功，状态码200"""
        self.project_list.click_add_project()
        self.project_list.fill_add_project('aaa', '', '')
        self.project_list.page.route(**mock_project_200)
        self.project_list.click_save_add_project()
        # 断言模态框隐藏
        expect(self.project_list.locator_add_modal).not_to_be_visible()

    def test_search_project_ajax(self):
        """项目列表搜索功能，断言ajax请求"""
        self.project_list.search_project_fill('test')
        with self.project_list.page.expect_request('**/api/project**') as req:
            self.project_list.click_search_btn()
        print('request: '+str(req.value))
        # 断言请求参数
        assert 'project_name=test' in req.value.url
        assert req.value.method == "GET"

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

    def test_refresh(self):
        """项目列表刷新功能，点刷新按钮查询请求"""
        with self.project_list.page.expect_request('**/api/project**') as req:
            self.project_list.click_refresh()
        # 断言请求参数
        assert 'page=1&size=15&project_name=&' in req.value.url
        assert req.value.method == "GET"
        assert False

    def test_link(self):
        """表格行内的链接"""
        # 造数据，mock 行内数据
        self.project_list.page.route(**mock_search_project_1)
        # 刷新页面
        self.project_list.page.reload()
        # 断言链接的属性和指向
        # 这里的id必须要和mock里面的id一致
        # 故意写成了不一致，所以会报错
        expect(self.project_list.locator_table_link_debugtalk).to_have_attribute('href','debugtalk.html?project_id=3046')

    def test_table_delete(self):
        """表格内删除。无法删除，需要管理员权限"""
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
        # # 方案二：直接按报错文本找新弹窗，自动忽略旧的残留弹窗
        # expect(self.project_list.page.get_by_text('操作异常："无权限操作，请联系管理员"')).to_be_visible()

    def test_table_edit(self):
        """表格行内编辑"""
        # 造数据，mock 行内数据
        self.project_list.page.route(**mock_search_project_1)
        # 重新刷新页面
        self.project_list.page.reload()
        # 注意，表格同一行中有两个地方，鼠标悬浮时都会出现“编辑”，两处点击效果是一样的
        # 所以，要加上first，定位其中一个
        self.project_list.locator_table_edit.first.click()
        # 断言模态框出现
        expect(self.project_list.locator_edit_modal).to_be_visible()