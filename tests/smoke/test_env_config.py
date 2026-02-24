def test_env_is_loaded(env_name: str, env_config: dict) -> None:
    assert env_config["environment"] == env_name
    assert env_config["base_url"].startswith("https://")
