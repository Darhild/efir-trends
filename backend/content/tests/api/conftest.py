import pytest

from content.app import create_app


@pytest.fixture
def app(temp_db):
    app = create_app(temp_db)
    return app
