import json
import os
from typing import Optional, Callable

import redis
import rq
from rq import Worker
from rq.serializers import JSONSerializer as RQJSONSerializer

from core.interface import IConsumer, type_consumer_id, Channelable
from utils.singleton import Singleton

OptionalRedisQueue = Optional[rq.Queue]

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)


class RedisConsumer(IConsumer, Singleton):
    """Redis consumer instantiated only once.

    However, multiple consumers with unique ids can be instantiated.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.redis_conn = redis.Redis(host=redis_host, port=redis_port, **kwargs)

    def setup(
            self, channel: Optional[Channelable] = None, **kwargs
    ) -> type_consumer_id:
        """Set up the consumer."""
        worker_id = kwargs.pop("worker_id", None)
        queue = rq.Queue(
            name=channel, connection=self.redis_conn, serializer=RQJSONSerializer, **kwargs
        )
        if worker_id:
            self._start_worker(queue, worker_id=worker_id)
        return queue.key

    def consume(self, consumer_id: type_consumer_id, data: dict, **optional_attrs) -> None:
        """Consume input."""
        callback_args = {}
        function_ref: Optional[Callable] = optional_attrs.get("function_ref")
        queue = rq.Queue.from_queue_key(consumer_id, connection=self.redis_conn)
        json_data = json.dumps(data)
        on_success_callback: Optional[Callable] = optional_attrs.get("on_success_callback")
        on_failure_callback: Optional[Callable] = optional_attrs.get("on_failure_callback")
        if on_success_callback:
            callback_args |= dict(on_success=on_success_callback)
        if on_failure_callback:
            callback_args |= dict(on_failure=on_failure_callback)
        if not function_ref:
            function_ref = (lambda result: result)
        queue.enqueue(function_ref, json_data, **callback_args)

    def _start_worker(self, r_queue: rq.Queue, /, worker_id=None) -> None:
        """Start a worker."""
        worker = self._find_worker(worker_id) if worker_id else None
        if worker:
            worker.queues += [r_queue]
            worker.refresh()
        else:
            worker = Worker([r_queue], connection=self.redis_conn, name=worker_id)
            worker.work()

    def _find_worker(self, worker_id) -> Optional[Worker]:
        workers = Worker.all(self.redis_conn)
        for worker in workers:
            if worker.name == worker_id:
                return worker
