import pytest
from app import validate_ticket, app

def test_title_too_long():
    ticket = {
        "title": "A" * 21,
        "room": "A101",
        "description": "测试内容"
    }
    ok, msg = validate_ticket(ticket)
    assert ok is False

    assert "标题不能超过20个字符" in msg

# 课15新增测试
def test_index_page():
    # 获取测试客户端

    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200

def test_new_ticket_page():
    client = app.test_client()
    resp = client.get("/tickets/new")
    assert resp.status_code == 200

def test_post_ticket_title_too_long():
    client = app.test_client()
    resp = client.post("/tickets/new", data={
        "title": "A"*21,
        "room": "A102",
        "description": "超长标题测试"
    })
    # 超长标题，返回400
    assert resp.status_code == 400
    assert "标题不能超过20个字符" in resp.data.decode("utf-8")

def test_post_ticket_valid():
    client = app.test_client()
    resp = client.post("/tickets/new", data={
        "title": "正常工单",
        "room": "A103",
        "description": "合法表单提交"
    })
    # 校验通过，重定向 302
    assert resp.status_code == 302
# --------课16新增：参数化边界测试--------
@pytest.mark.parametrize("title,expected", [
    ("正常标题", 302),
    ("A" * 19, 302),
    ("A" * 20, 302),
    ("A" * 21, 400),
    ("A" * 100, 400),
])
def test_title_boundary(client, title, expected):
    resp = client.post("/tickets/new", data={
        "title": title,
        "room": "A区101",
        "description": "测试",
    })
    assert resp.status_code == expected
