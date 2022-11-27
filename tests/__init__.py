import pytest
from datawarehouse import create_app


@pytest.fixture(scope="session")
def session():
    from datawarehouse.config.db import config

    yield config.session


@pytest.fixture(scope="session")
def engine():
    from datawarehouse.config.db import config

    yield config.engine


@pytest.fixture(scope="session")
def test_app():
    app = create_app(config="TestingConfig")
    return app.test_client()
