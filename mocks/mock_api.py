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