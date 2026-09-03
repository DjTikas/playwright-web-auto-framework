# cases/common/validation_data.py —— 只描述「业务规则」，不碰任何页面细节
FORM_VALIDATION_CASES = [
    # (字段, 非法输入, 期望提示关键字)
    ("username", "",            "不能为空"),
    ("username", "x" * 31,     "1-30位字符"),
    ("username", "daij@",       "不能有特殊字符"),
    ("password", "",            "不能为空"),
    ("password", "123",         "6-16位字符"),
    ("password", "123" * 10,    "6-16位字符"),
    ("password", "123456aa*-", "不能有特殊字符"),
]