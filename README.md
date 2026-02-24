# API 自动化测试项目骨架（Pytest + Allure）

该项目提供了一个可扩展的接口自动化基础结构，支持三套运行环境：

- 测试环境：`test`
- 预发布环境：`preprod`
- 生产环境：`prod`

## 目录结构

```text
.
├── project/
│   ├── config/
│   │   └── env/
│   │       ├── test.yaml
│   │       ├── preprod.yaml
│   │       └── prod.yaml
│   ├── framework/
│   │   └── config.py
│   └── tests/
│       ├── conftest.py
│       └── smoke/
│           └── test_env_config.py
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
