#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
"""
This module provides generic AMQP daemon and builder of common connection
informations, which are defined as constants in :mod:`edeposit.amqp.settings`.

Daemon is used by :mod:`edeposit.amqp.alephdaemon` and
:mod:`edeposit.amqp.calibredaemon`.
"""
import pika

try:
    import edeposit.amqp.serializers as serializers
except ImportError:
    import serializers

import pikadaemon
import settings


#= Functions & objects ========================================================
def getConParams(virtualhost):
    """
    Connection object builder.

    Args:
        virtualhost (str): selected virtualhost in rabbitmq

    Returns:
        pika.ConnectionParameters: object filled by `constants` from
        :class:`edeposit.amqp.settings`.
    """
    return pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=int(settings.RABBITMQ_PORT),
        virtual_host=virtualhost,
        credentials=pika.PlainCredentials(
            settings.RABBITMQ_USER_NAME,
            settings.RABBITMQ_USER_PASSWORD
        )
    )


class AMQPDaemon(pikadaemon.PikaDaemon):
    def __init__(self, con_param, queue, out_exch, out_key, react_fn, glob):
        """
        Args:
            con_param (ConnectionParameters): see :func:`getConParams` for
                                              details
            queue (str):    name of the queue
            out_exch (str): name of the exchange for outgoing messages
            out_key (str):  what key will be used to send messages back
            react_fn (fn):  function, which can react to messages, see Note for
                            details
            glob (dict):    result of ``globals()`` call - used in deserializer
                            to automatically build classes, which are not
                            available in this namespace of this package

        Note:
            ``react_fn`` parameter is expected to be function, which gets three
            parameters - `message` (some form of message, it can be also
            namedtuple), `response_callback` (function expecting `message` and
            `UUID` parameters which is used to send response) and `UUID`.

        Example of function used as `react_fn` parameter::

            def reactToAMQPMessage(message, response_callback, UUID):
                response = None
                if message == 1:
                    response = 2
                elif message == "Hello":
                    response = "Hi"
                elif type(message) == dict:
                    reponse = {1: 2}

                if not reponse:
                    raise UserWarning("Unrecognized message")

                return response_callback(response, UUID)

        As you can see, protocol is pretty easy. You get `message`, you
        create `response`, in which you react to `message` and you send
        it back using `response_callback` parameter.

        Note:
            It is better if you ``return`` value from `response_callback` call
            back. You will appreciate this during debugging phase of you
            project.


        """
        super(AMQPDaemon, self).__init__(
            con_param, queue, out_exch, out_key
        )

        self.react_fn = react_fn
        self.globals = glob

    def onMessageReceived(self, method_frame, properties, body):
        """
        React to received message - deserialize it, add it to users reaction
        function stored in ``self.react_fn`` and send back result.

        If `Exception` is thrown during process, it is sen't back instead of
        message.

        Note:
            In case of `Exception`, response message doesn't have useful `body`,
            but in headers is stored this parameters: `exception`, where the
            Exception's message is stored, `exception_type`, where
            ``e.__class__`` is stored and ``exception_name``, where
            ``e.__class__.__name__`` is stored.

            This allows you to react to unexpected cases at the other end of
            the AMQP communication.
        """
        # if UUID is not in headers, just ack the message and ignore it
        if "UUID" not in properties.headers:
            return True  # ack message

        try:
            self.react_fn(
                serializers.deserialize(body, self.globals),
                self.sendResponse,
                properties.headers["UUID"]
            )
        except Exception, e:
            # get informations about message
            msg = e.message if hasattr(e, "message") else str(e)
            exception_type = str(e.__class__)
            exception_name = str(e.__class__.__name__)

            self.sendMessage(
                self.output_exchange,
                settings.RABBITMQ_ALEPH_EXCEPTION_KEY,
                str(e),
                properties=pika.BasicProperties(
                    content_type="application/text",
                    delivery_mode=2,
                    headers={
                        "exception": msg,
                        "exception_type": exception_type,
                        "exception_name": exception_name
                    }
                )
            )

        return True  # ack message

    def sendResponse(self, message, UUID):
        """
        Send `message` with given `UUID` back to the queue defined in
        `self.output_exchange` with `self.output_key`.
        """
        super(AMQPDaemon, self).sendResponse(
            serializers.serialize(message),
            UUID
        )
