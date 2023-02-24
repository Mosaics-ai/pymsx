"""Test pymsx

Test application config.
"""


def test_env_config(monkeypatch):
    """Text env variables setting config."""
    with monkeypatch.context() as m:
        test_email = "test_email"
        test_password = "test_password"
        base_url = "http://localhost:8080"

        m.setenv("MSX_EMAIL", test_email)
        m.setenv("MSX_PASSWORD", test_password)
        m.setenv("MSX_BASE_URL", base_url)

        from pymsx.config import app_config

        config = app_config()

        assert config.email == test_email
        assert config.password == test_password
        assert config.base_url == base_url
