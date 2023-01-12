"""Integration-Test suite for redis consumer."""
import pytest
import logging
from core.interface import type_consumer_id

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

    async def test_redis_setup(self, caplogger, redis_session) -> None:
        """Test the redis consumer setup."""
        redis_session.redis_conn.ping()
        # To bypass worker, see: https://python-rq.org/docs/#bypassing-workers
        consumer_queue_key = await redis_session.setup(channel="radio", is_async=False)
        assert isinstance(consumer_queue_key, str)

    def test_redis_consume(self) -> None:
        """Test the redis consumer."""
        assert 1
