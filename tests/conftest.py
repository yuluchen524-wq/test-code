import os

import pytest

from framework.config import load_env_config
from framework.http import ApiClient


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default=os.getenv("TEST_ENV", "test"),
        help="Run environment: test | preprod | prod (default: test)",
    )
    parser.addoption(
        "--alluredir",
        action="store",
        default="reports/allure-results",
        help="Allure output directory (works when allure plugin is installed)",
    )


@pytest.fixture(scope="session")
def env_name(pytestconfig: pytest.Config) -> str:
    return pytestconfig.getoption("--env")


@pytest.fixture(scope="session")
def env_config(env_name: str) -> dict:
    return load_env_config(env_name)


@pytest.fixture(scope="session")
def base_url(env_config: dict) -> str:
    return env_config["base_url"]


@pytest.fixture(scope="session")
def api_client(env_config: dict) -> ApiClient:
    client = ApiClient(
        base_url=env_config["base_url"],
        timeout=int(env_config.get("timeout", 10)),
    )
    yield client
    client.close()
