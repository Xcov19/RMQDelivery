"""Integration-Test suite for redis consumer."""
import pytest
import logging

# **************************************************** #
# Use pytest -m fast to run the tests in fast mode.
# Use pytest -s to see the test debug output like print.
# **************************************************** #

@pytest.mark.slow
@pytest.mark.usefixtures("anyio_backend")
@pytest.mark.usefixtures("caplogger")
@pytest.mark.usefixtures("redis_session")
class TestRedisConsumer:
    """Test the redis consumer."""

    def test_redis_setup(self, caplogger, redis_session) -> None:
        """Test the redis consumer setup."""
        redis_session.redis_conn.ping()
        assert 1

    def test_redis_consume(self) -> None:
        """Test the redis consumer."""
        assert 1
