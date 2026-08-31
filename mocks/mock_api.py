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
                    "id": 1111,
                    "project_name": "test_module",
                    "publish_app": "",
                    "project_desc": "",
                    "active": "1",
                    "create_time": "2023-03-02 11:30:00",
                    "update_time": "2023-03-02 11:30:00",
                    "test_user": "daij"
                },
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

"""
    模拟模块列表页的表格内容 1
"""
mock_module_list_table_page_1 = {
    "url": "**/api/module**",
    'handler': lambda route: route.fulfill(
        status = 200,
        body=json.dumps({
            "total": 28,
            "rows": [
                {
                    "id": 123,
                    "module_name": "123aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 122,
                    "module_name": "122aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 121,
                    "module_name": "121aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 120,
                    "module_name": "120aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 119,
                    "module_name": "119aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 118,
                    "module_name": "118aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 117,
                    "module_name": "117aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 116,
                    "module_name": "116aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 115,
                    "module_name": "115aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 114,
                    "module_name": "114aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 113,
                    "module_name": "113aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 112,
                    "module_name": "112aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 111,
                    "module_name": "111aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 110,
                    "module_name": "110aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 109,
                    "module_name": "109aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                }
            ]
        })
    )
}


"""
    模拟模块列表页的表格内容 2
"""
mock_module_list_table_page_2 = {
    "url": "**/api/module**",
    'handler': lambda route: route.fulfill(
        status = 200,
        body=json.dumps({
            "total": 25,
            "rows": [
                {
                    "id": 108,
                    "module_name": "108aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 107,
                    "module_name": "107aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 106,
                    "module_name": "106aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 105,
                    "module_name": "105aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 104,
                    "module_name": "104aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 103,
                    "module_name": "103aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 102,
                    "module_name": "102aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 101,
                    "module_name": "101aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 100,
                    "module_name": "100aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 99,
                    "module_name": "99aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                }
            ]
        })
    )
}

"""
    模拟模块列表页的表格内容 10行
"""
mock_module_list_table_10_row = {
    "url": "**/api/module**",
    'handler': lambda route: route.fulfill(
        status = 200,
        body=json.dumps({
            "total": 28,
            "rows": [
                {
                    "id": 123,
                    "module_name": "123aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 122,
                    "module_name": "122aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 121,
                    "module_name": "121aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 120,
                    "module_name": "120aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 119,
                    "module_name": "119aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 118,
                    "module_name": "118aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 117,
                    "module_name": "117aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 116,
                    "module_name": "116aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 115,
                    "module_name": "115aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                },
                {
                    "id": 114,
                    "module_name": "114aaa",
                    "project_id": 1111,
                    "test_user": "daij",
                    "module_desc": "",
                    "create_time": "2026-08-22 19:54:56",
                    "update_time": "2026-08-22 19:54:56",
                    "project_name": "test_module"
                }
            ]
        })
    )
}

"""
    模拟添加环境已存在，返回400
"""
mock_add_env_400 = {
    'url': '**api/env',
    'handler': lambda route: route.fulfill(
        status=400,
        body=({
            "errors": {
                "env_name": "env_name: test123 已存在"
            },
            "message": "Input payload validation failed"
        })
    )
}

"""
    模拟添加环境成功，返回200
"""
mock_add_env_200 = {
    'url': '**api/env',
    'handler': lambda route: route.fulfill(
        status=200,
        body=({
            "code": 0,
            "message": "success",
            "data": {
                "id": 30,
                "env_name": "test2026",
                "base_url": "http://www.baidu.com",
                "simple_desc": "",
                "env_code": "",
                "test_user": "daij",
                "create_time": "2026-08-27 16:12:34",
                "update_time": "2026-08-27 16:12:34"
            }
        })
    )
}