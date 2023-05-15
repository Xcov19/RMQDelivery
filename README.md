## TL;DR
A redis based queueing and streaming package built on redis queue package `rq` and redis `streams` or redis `pubsub`.

This is a wrapper around `rq` and `redis-py` to provide a simple interface to enqueue and dequeue messages from a queue and stream messages from a channel.

Any service can use it to create:
- a dedicated queue channel and;
- a dedicated consumer group for streaming so that external services can consume from dedicated channels.

### Motivation

We need an at-least once delivery mechanism using:
- a custom enqueue/dequeue and
- publish/pull service using streams.


It is exciting because it can be dropped in for
testing with in-house development and can be
deployed by anyone with easy to use abstract
interfaces and can be forked, built on-top of
redis ecosystem, no need to explore beyond the
redis stack.

![image info](overview.png)

### Direct & Indirect Dependencies:
- redis-py
- redis-om-python
- rq

<hr />

### References

- [Redis Streams](https://aws.amazon.com/redis/Redis_Streams/)
- [Redis Streams core commands](https://redis-py.readthedocs.io/en/stable/commands.html?highlight=xadd#redis.commands.core.CoreCommands.xadd)
- [Using Redis Stream with Python](https://huogerac.hashnode.dev/using-redis-stream-with-python)
