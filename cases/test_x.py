# 使用共享上下文（已登录）
import allure


def test_shared_demo_1(shared_page):
    with allure.step("执行用例步骤"):
        shared_page.goto("/index.html")
        assert False


def test_shared_demo_2(shared_page):
    with allure.step("执行用例步骤"):
        shared_page.goto("/list_project.html")
        assert False

# 使用无登录隔离上下文（注册登录页）
def test_unlogin_demo_1(unlogin_page):
    unlogin_page.goto("/login.html")
    assert False

def test_unlogin_demo_2(unlogin_page):
    unlogin_page.goto("/register.html")
    assert False