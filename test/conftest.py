import logging
from typing import Any

import pytest
from pytest import FixtureRequest


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
@pytest.fixture(scope="function", autouse=True)
def caplogger(caplog: Any) -> Any:
    caplog.set_level(logging.ERROR, logger="test.test_redis_consumer")
    return caplog
