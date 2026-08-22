import json

"""
    模拟新增项目，返回 400
"""
mock_project_400 = {
    "url": "**/api/project",
    "handler": lambda route: route.fulfill(
        status = 400,
        body=json.dumps({
            "errors": {
                "project_name": "test 已存在"
            },
            "message": "Input payload validation failed"
        })
    )
}

"""
    模拟新增项目，返回 500
"""
mock_project_500 = {
    "url": "**/api/project",
    "handler": lambda route: route.fulfill(
        status = 500,
        body="服务器错误"
    )
}

"""
    模拟新增项目成功，返回 200
"""
mock_project_200 = {
    "url": "**/api/project",
    "handler": lambda route: route.fulfill(
        status = 200,
        body=json.dumps({
            "code": 0,
            "message": "success",
            "data": {
                "id": 3047,
                "project_name": "132456aaaa",
                "publish_app": "",
                "project_desc": "",
                "active": "1",
                "create_time": "2026-08-21 13:13:13",
                "update_time": "2026-08-21 13:13:13",
                "test_user": "daij"
            }
        })
    )
}

"""
    模拟搜素项目，返回0个结果
"""
mock_search_project_0 = {
    "url": "**/api/project**",
    "handler": lambda route: route.fulfill(
        status = 200,
        body=json.dumps({
            "total": 0,
            "rows": []
        })
    )
}

"""
    模拟搜素项目，返回1个结果
"""
mock_search_project_1 = {
    "url": "**/api/project**",
    "handler": lambda route: route.fulfill(
        status = 200,
        body=json.dumps({
            "total": 1,
            "rows": [
                {
                    "id": 1,
                    "project_name": "test",
                    "publish_app": "",
                    "project_desc": "",
                    "active": "1",
                    "create_time": "2026-08-21 11:37:11",
                    "update_time": "2026-08-21 11:37:11",
                    "test_user": "daij"
                }
            ]
        })
    )
}

"""
    模拟删除项目失败，返回 403
"""
# 注意url，一定要写成"**/api/project/**"
# 不能写成"**/api/project**"，否则会匹配到错误的接口
mock_project_delete_403 = {
    "url": "**/api/project/**",
    "handler": lambda route: route.fulfill(
        status = 403,
        body=json.dumps({
            "message": "无权限操作，请联系管理员"
        })
    )
}


"""
/**** 模拟新增模块 项目选项 ***/
"""
mock_project_select_200 = {
    "url": "**/api/project",
    "handler": lambda route: route.fulfill(
        status=200,
        body=json.dumps({
            "total": 9,
            "rows": [
                {
                    "id": 53,
                    "project_name": "test",
                    "publish_app": "",
                    "project_desc": "",
                    "active": "1",
                    "create_time": "2023-03-02 11:30:00",
                    "update_time": "2023-03-02 11:30:00",
                    "test_user": "py"
                },
                {
                    "id": 43,
                    "project_name": "hello",
                    "publish_app": "xx",
                    "project_desc": "xxx",
                    "active": "1",
                    "create_time": "2023-03-01 22:06:05",
                    "update_time": "2023-03-01 22:06:05",
                    "test_user": "py"
                }, {
                    "id": 42,
                    "project_name": "world",
                    "publish_app": "xx",
                    "project_desc": "xxx",
                    "active": "1",
                    "create_time": "2023-03-01 21:30:06",
                    "update_time": "2023-03-01 21:30:06",
                    "test_user": "py"
                }, {
                    "id": 41,
                    "project_name": "测试项目",
                    "publish_app": "xx",
                    "project_desc": "xxx",
                    "active": "1",
                    "create_time": "2023-03-01 21:29:35",
                    "update_time": "2023-03-01 21:29:35",
                    "test_user": "py"
                }]
        })
    )
}


"""
    模拟新增模块名重复，返回400
"""
mock_module_repeat_400 = {
    "url": "**/api/module",
    'handler': lambda route: route.fulfill(
        status = 400,
        body=json.dumps({
            "message": "module_name: test 已存在"
        })
    )
}

"""
    模拟新增模块成功，返回201
"""
mock_add_module_201 = {
    "url": "**/api/module",
    'handler': lambda route: route.fulfill(
        status = 201,
        body=json.dumps({
            "code": 0,
            "message": "success",
            "data": {
                "id": 103,
                "module_name": "testxx",
                "project_id": 53,
                "test_user": "py",
                "module_desc": "",
                "create_time": "2026-08-22 19:54:56",
                "update_time": "2026-08-22 19:54:56",
                "project_name": "test"
            }
        })
    )
}
