"""Unit-Test suite for redis consumer."""
import pytest

# **************************************************** #
# Use pytest -m fast to run the tests in fast mode.
# Use pytest -s to see the test debug output like print.
# **************************************************** #

@pytest.mark.fast
@pytest.mark.usefixtures("anyio_backend")
@pytest.mark.usefixtures("caplogger")
class TestRedisConsumer:
    """Test the redis consumer."""

    def test_redis_consumer(self) -> None:
        """Test the redis consumer."""
        assert 1
