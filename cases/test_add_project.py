import uuid

import pytest
from playwright.sync_api import Page, expect

from mocks import mock_api
from pages.add_project_page import AddProjectPage


class TestAddProject:
    """新增项目页"""
    @pytest.fixture(autouse=True)
    def start_for_each(self, login_prepare, shared_page: Page):
        print("for each--start: 打开添加项目页")
        self.add_project = AddProjectPage(shared_page)
        self.add_project.navigate()
        yield
        print("for each--end: 后置操作")

    def test_add_project_1(self):
        """项目名为空，提交失败"""
        self.add_project.fill_project_name('')
        self.add_project.fill_project_desc('')
        self.add_project.fill_publish_app('')
        self.add_project.click_submit_btn()
        # 断言 按钮不可点击
        expect(self.add_project.locator_submit_btn).to_be_disabled()

    @pytest.mark.parametrize('name, app, desc, title', [
        ['test@*', '', '', '项目名称包含特殊字符'],
        ['123456789012345687901234567890123456', '', '', '项目名称超过30位'],
        ['test', 'zzz*@4g', '', '所属应用包含特殊字符'],
        ['test', '123456789012345687901234567890123456', '', '所属应用超过30位'],
        ['test', '', '出师表', '项目描述超过200位']
    ])
    def test_add_project_2(self, name, app, desc, title):
        """信息填写不符合规范，无法点击提交"""
        self.add_project.fill_project_name(name)
        self.add_project.fill_publish_app(app)
        if desc == '出师表':
            desc = """
            先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。

　　宫中府中，俱为一体；陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。

　　侍中、侍郎郭攸之、费祎、董允等，此皆良实，志虑忠纯，是以先帝简拔以遗陛下。愚以为宫中之事，事无大小，悉以咨之，然后施行，必能裨补阙漏，有所广益。

　　将军向宠，性行淑均，晓畅军事，试用于昔日，先帝称之曰能，是以众议举宠为督。愚以为营中之事，悉以咨之，必能使行阵和睦，优劣得所。

　　亲贤臣，远小人，此先汉所以兴隆也；亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓、灵也。侍中、尚书、长史、参军，此悉贞良死节之臣，愿陛下亲之信之，则汉室之隆，可计日而待也。

　　臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。后值倾覆，受任于败军之际，奉命于危难之间，尔来二十有一年矣。

　　先帝知臣谨慎，故临崩寄臣以大事也。受命以来，夙夜忧叹，恐托付不效，以伤先帝之明；故五月渡泸，深入不毛。今南方已定，兵甲已足，当奖率三军，北定中原，庶竭驽钝，攘除奸凶，兴复汉室，还于旧都。此臣所以报先帝而忠陛下之职分也。至于斟酌损益，进尽忠言，则攸之、祎、允之任也。

　　愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道，察纳雅言，深追先帝遗诏。臣不胜受恩感激。今当远离，临表涕零，不知所言。
            """
        self.add_project.fill_project_desc(desc)
        # 断言 按钮不可点击
        expect(self.add_project.locator_submit_btn).to_be_disabled()

    def test_add_project_400(self, shared_page):
        """项目已存在，弹出模态框，400状态码"""
        self.add_project.fill_project_name('test')
        # mock 接口返回400
        shared_page.route(**mock_api.mock_project_400)
        self.add_project.click_submit_btn()
        # 校验结果 弹出框文本包含
        expect(self.add_project.locator_bootbox).to_be_visible()
        expect(self.add_project.locator_bootbox).to_contain_text('已存在')

    def test_add_project_500(self, shared_page):
        """服务器异常，500状态码"""
        self.add_project.fill_project_name('test')
        # mock 接口返回500
        shared_page.route(**mock_api.mock_project_500)
        self.add_project.click_submit_btn()
        # 校验结果 弹出框文本包含
        expect(self.add_project.locator_bootbox).to_be_visible()
        expect(self.add_project.locator_bootbox).to_contain_text('操作异常')

    def test_add_project_success(self):
        """添加成功，跳转到项目列表页面"""
        self.add_project.fill_project_name(str(uuid.uuid4())[:8])
        self.add_project.click_submit_btn()
        expect(self.add_project.page).to_have_title('项目列表')
        expect(self.add_project.page).to_have_url('/list_project.html')

    def test_add_project_success_2(self):
        """添加成功，判断项目列表页面中存在新增的项目"""
        project_name = str(uuid.uuid4())[:8]
        self.add_project.fill_project_name(project_name)
        self.add_project.click_submit_btn()
        # 点击保存后等页面重定向到table表格页
        self.add_project.page.wait_for_load_state('networkidle')
        # 等待表格DOM出现，再去all拿元素，减少偶发空列表
        self.add_project.page.locator("#table").wait_for()
        # 断言新增项目在列表页
        print(f"新增项目名称: {project_name}")
        # 获取页面 table 表格-项目名称列全部内容
        locator_projects = self.add_project.page.locator(
            '//table[@id="table"]//td[3]/a'
        )
        project_name_list = [i.inner_text() for i in locator_projects.all()]
        print(project_name_list)
        assert project_name in project_name_list


