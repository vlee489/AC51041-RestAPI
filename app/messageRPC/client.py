"""
RabbitMQ RPC Client

based off of https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/6-rpc.html
"""
import asyncio
import uuid
import logging
from typing import MutableMapping
from aio_pika import Message, connect
from aio_pika.abc import (AbstractChannel, AbstractConnection, AbstractIncomingMessage, AbstractQueue)
import ormsgpack

from .response import Response


class Client:
    connection: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue
    loop: asyncio.AbstractEventLoop

    def __init__(self, uri: str) -> None:
        """
        Init
        :param uri: Connection URI
        """
        self.__uri = uri
        self.futures: MutableMapping[str, asyncio.Future] = {}
        self.loop = asyncio.get_running_loop()

    async def connect(self) -> "Client":
        """
        Connect to RabbitMQ
        :return: Client
        """
        self.connection = await connect(self.__uri, loop=self.loop)
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.on_response)
        return self

    def on_response(self, message: AbstractIncomingMessage) -> None:
        """
        On response from RPC consumer
        :param message: Incoming message
        :return: Dict response
        """
        if message.correlation_id is None:
            logging.error(f"Bad RPC Response: {message!r}")
            return
        future: asyncio.Future = self.futures.pop(message.correlation_id)
        response = ormsgpack.unpackb(message.body)
        future.set_result(response)

    async def call(self, routing_key: str, payload: dict) -> Response:
        """
        Send RPC Call
        :param routing_key: routing key for RabbitMQ
        :param payload: Message payload dict
        :return: Dict response from consumer
        """
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()
        self.futures[correlation_id] = future
        payload = ormsgpack.packb(payload)

        await self.channel.default_exchange.publish(
            Message(
                payload,
                content_type="json/msgpack",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key=routing_key
        )
        return Response(await future)
