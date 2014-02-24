"""
Purpose of this module is to provide class for launching unix daemons
(daemonwrapper.py), AMQP communication service based on rabbitmq's pika library
(pikadaemon.py) and also AMQP communication classes for specific modules used
in edeposit project (so far, there is only communication with the Aleph in
alephdaemon.py).

alephdaemon module allows you to send simple requests to get data from Aleph
(system used in libraries all around the world) and in later versions also
requests to put data into Aleph. Details of protocol and communication with
Aleph server are handled by edeposit.amqp.aleph module:

    https://github.com/jstavel/edeposit.amqp.aleph

= Request =====================================================================
You just have to send serialized one of the Request classes, which are defined
in aleph's __init__.py, into the rabbitmq's exchange defined in
settings.RABBITMQ_ALEPH_EXCHANGE. Serialization can be done by calling module's
.serialize() property.

Example showing how to send data to proper exchange:

---
import uuid

import settings
from alephdaemon import getConnectionParameters

connection = pika.BlockingConnection(alephdaemon.getConnectionParameters())
channel = connection.channel()

UUID = uuid.uuid4()  # this will be used to pair request with response

# put request together
json_data = aleph.serialize(
    aleph.SearchRequest(
        aleph.ISBNQuery("80-251-0225-4")
    )
)

# create properties of message - notice particularly the UUID parameter
properties = pika.BasicProperties(
    content_type="application/json",
    delivery_mode=1,
    headers={"UUID": str(UUID)}
)

# send the message to proper exchange with proper routing key
channel.basic_publish(
    exchange=settings.RABBITMQ_ALEPH_EXCHANGE,
    routing_key=settings.RABBITMQ_ALEPH_DAEMON_KEY,
    properties=properties,
    body=json_data
)
---

It looks kinda long, but it is really simple and the most important thing in
respect to communication with module is:

---
json_data = aleph.serialize(
    aleph.SearchRequest(
        aleph.ISBNQuery("80-251-0225-4")
    )
)
---

Here you say, that you want to perform SearchRequest and specifically search
for ISBN.

Another important thing is to send and save for later use the UUID. You want to
do this to be able to pair the response with request. Also messages received
without UUID are thrown away without any warning.

Notice also the `routing_key` parameter of channel.basic_publish(). It is used
to determine into which queue will be message delivered.

= Response ====================================================================
Response message is sent into settings.RABBITMQ_ALEPH_EXCHANGE with routing key
settings.RABBITMQ_ALEPH_PLONE_KEY.

Format of response is usually one of the Reponse classes from aleph.__init__.py
In headers, there should always be the UUID parameter, even in case of some
unexpected error.

You can detect errors by looking for "exception" key in parameters.headers
dictionary:

---
for method_frame, properties, body in self.channel.consume(self.queue):
    headers = properties.headers
    if "exception" in headers:
        print "There was an error in processing request ", headers["UUID"]
        print headers["exception_name"] + ": " + headers["exception"]
        break
---

Details of exception are contained in "exception", "exception_name" and
"exception_type" keys. First is text of error message, second is the
.__class__.__name__ of exception and thid is just output from type(exception).
"""
