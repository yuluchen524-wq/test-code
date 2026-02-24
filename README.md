# API 自动化测试项目骨架（Pytest + Allure）

该项目提供了一个可扩展的接口自动化基础结构，支持三套运行环境：

- 测试环境：`test`
- 预发布环境：`preprod`
- 生产环境：`prod`

## 目录结构

```text
.
├── config/
│   └── env/
│       ├── test.yaml
│       ├── preprod.yaml
│       └── prod.yaml
├── framework/
│   ├── config.py
│   └── http/
│       └── client.py
├── tests/
│   ├── conftest.py
│   ├── smoke/
│   │   └── test_env_config.py
│   └── unit/
│       └── test_api_client.py
├── pytest.ini
└── requirements.txt
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行方式

默认执行测试环境（`test`）：

```bash
pytest
```

指定环境执行：

```bash
pytest --env=preprod
pytest --env=prod
```

也可以通过环境变量设置：

```bash
TEST_ENV=preprod pytest
```

## Allure 报告

执行完成后结果在：`reports/allure-results`

生成和打开报告示例：

```bash
allure serve reports/allure-results
```


## 接口自动化基础能力

当前已内置基础 `ApiClient`（`framework/http/client.py`），在 `tests/conftest.py` 中提供了会话级别 fixture：

- `api_client`: 自动读取当前环境 `base_url` 与 `timeout`，用于统一发起 HTTP 请求。

示例（在测试中直接使用）：

```python
def test_example(api_client):
    resp = api_client.get("/ping")
    assert resp.status_code == 200
```
