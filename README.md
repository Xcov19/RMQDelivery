## TL;DR
A redis based queueing and streaming package built on redis queue package `rq` and redis `streams` or redis `pubsub`.

Any service can use it to create a dedicated queue and dedicated consumer group for streaming so that external services can consume from dedicated channels.

### Motivation

We need a custom zapier like enqueue/push and pull/stream/publish service with at-least once delivery using streams or at-most once delivery using lightweight redis pub-sub depending on the use case.

It is exciting because it is in-house and can be deployed by anyone with easy to use abstract interfaces and can be forked, built-on top of.


### Direct & Indirect Dependencies:
- redis-py
- redis-om-python
- rq

<hr />

### References

- [Redis Streams](https://aws.amazon.com/redis/Redis_Streams/)
- [Redis Streams core commands](https://redis-py.readthedocs.io/en/stable/commands.html?highlight=xadd#redis.commands.core.CoreCommands.xadd)
- [Using Redis Stream with Python](https://huogerac.hashnode.dev/using-redis-stream-with-python)
