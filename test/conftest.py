import os
import logging
from typing import Any

import pytest
from pytest import FixtureRequest

from infrastructure.redis_lib import RedisConsumer

pytest_logger = logging.getLogger(__file__)
pytest_logger.setLevel(logging.INFO)

# ************************************************* #
# Setup pytest anyio fixture.
# The anyio_backend fixture determines the backends
# and their options that tests and fixtures are run with.
# The AnyIO pytest plugin comes with a function scoped
# fixture with this name which runs everything on all supported backends.
# ************************************************* #
@pytest.fixture(
    scope="session",
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ],
)
def anyio_backend(request: FixtureRequest.session) -> Any:  # type: ignore[no-any-unimported]
    return request.param


# ************************************************* #
# Setup a fixture caplog for unsuccessful tests.
# You can run pytest -ra -q to see only unsuccessful logs.
# ************************************************* #
@pytest.fixture(scope="function")
def caplogger(caplog: Any) -> Any:
    caplog.set_level(logging.ERROR, logger="test.test_redis_consumer")
    return caplog

# ************************************************* #
# Setup redis connection
# ************************************************* #
@pytest.fixture(scope="function")
def redis_session(caplogger):
    caplogger.set_level(logging.DEBUG, logger="test.test_redis_consumer")
    kwargs = {}
    if redis_pwd := os.getenv("REDIS_PASSWORD", None):
        kwargs |= dict(password=redis_pwd)
    pytest_logger.info("starting redis consumer session.")
    print("starting redis consumer session.")
    redis_consumer = RedisConsumer(**kwargs)
    yield redis_consumer
    pytest_logger.info("closing redis session.")
    print("closing redis session.")
    redis_consumer.close()
