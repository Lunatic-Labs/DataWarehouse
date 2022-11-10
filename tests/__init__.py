import pytest
from datawarehouse import create_app


@pytest.fixture(scope="session")
def test_app():
    app = create_app(config="TestingConfig")
    return app.test_client()
