"""Test pymoai

Test application config.
"""


def test_env_config(monkeypatch):
    """Text env variables setting config."""
    with monkeypatch.context() as m:
        test_email = "test_email"
        test_password = "test_password"
        base_url = "http://localhost:8080"

        m.setenv("MOAI_EMAIL", test_email)
        m.setenv("MOAI_PASSWORD", test_password)
        m.setenv("MOAI_BASE_URL", base_url)

        from pymoai.config import app_config

        config = app_config()

        assert config.email == test_email
        assert config.password == test_password
        assert config.base_url == base_url
