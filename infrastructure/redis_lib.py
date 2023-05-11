import json
import os
from typing import Optional, Callable

import redis
import rq
from rq import Worker
from rq.serializers import JSONSerializer as RQJSONSerializer

from core.interface import IConsumer, IProducer, type_consumer_id, Channelable
from utils.singleton import Singleton

OptionalRedisQueue = Optional[rq.Queue]


class RedisConsumer(IConsumer, Singleton):
    """Redis consumer instantiated only once.

    However, on same machine instance multiple consumers with same id can be instantiated
    which means they're all pointing to same RedisConsumer.
    Underneath, a redis consumer has many queues assigned to
    various worker-ids.

    Call like:
    redis_consumer = RedisConsumer(**redis_py_options)
    redis_consumer.setup(channel="sample_channel_announcements", worker_id=worker_id)
    redis_consumer.consume(
    consumer_channel_queue_key, raw_json_data, callback=callback, on_success_callback=on_success_callback, on_failure_callback=on_failure_callback)
    """

    def __init__(self, **kwargs):
        super().__init__()
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = os.getenv("REDIS_PORT", 6379)
        self.redis_conn = redis.Redis(host=redis_host, port=redis_port, **kwargs)

    def close(self):
        """Closes connection."""
        self.redis_conn.close()

    def setup(
        self, channel: Optional[Channelable] = None, **kwargs
    ) -> type_consumer_id:
        """Set up the consumer."""
        worker_id = kwargs.pop("worker_id", None)
        queue = rq.Queue(
            name=channel,
            connection=self.redis_conn,
            serializer=RQJSONSerializer,
            **kwargs,
        )
        if worker_id:
            # start or add queue to worker
            self._start_worker(queue, worker_id=worker_id)
        return queue.key

    def consume(
        self, consumer_id: type_consumer_id, data: dict, **optional_attrs
    ) -> None:
        """Consume input."""
        callback_args = {}
        queue = rq.Queue.from_queue_key(consumer_id, connection=self.redis_conn)
        callback: Optional[Callable] = optional_attrs.get("callback")
        if not callback:
            callback = lambda result: result
        on_success_callback: Optional[Callable] = optional_attrs.get(
            "on_success_callback"
        )
        on_failure_callback: Optional[Callable] = optional_attrs.get(
            "on_failure_callback"
        )
        if on_success_callback:
            callback_args |= dict(on_success=on_success_callback)
        if on_failure_callback:
            callback_args |= dict(on_failure=on_failure_callback)

        json_data = json.dumps(data)
        queue.enqueue(callback, json_data, **callback_args)

    def _start_worker(self, r_queue: rq.Queue, /, worker_id=None) -> None:
        """Start a worker or add queue to it."""
        if worker := self._find_worker(worker_id) if worker_id else None:
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


class RedisProducer(IProducer):
    ...
