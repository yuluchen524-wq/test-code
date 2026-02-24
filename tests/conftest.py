import os

import pytest

from framework.config import load_env_config


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
