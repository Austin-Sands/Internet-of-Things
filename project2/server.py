#!/usr/bin/env python
import datetime
import logging
import configparser
from w1thermsensor import W1ThermSensor

import asyncio

import aiocoap.resource as resource
import aiocoap


class HelloResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.set_content(b'<<Hello World>>')

    def set_content(self, content):
        self.content = content

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)
    
class TempResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.get_temp()

    def get_temp(self):
        sensor = W1ThermSensor()
        currentTemp = sensor.get_temperature()
        print("Current Temperature is %s C" %currentTemp)
        self.currentTemp = bytes(str(currentTemp), 'utf-8')

    async def render_get(self, request):
        return aiocoap.Message(payload=self.currentTemp)


# logging setup

default_config = {
    "host": "localhost",
}

def read_config(config_ini):
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(config_ini)

    if config.has_section("Server"):
        host = config["Server"]["host"]
        
        print("Server settings read from config:", host, sep=' ')
    else:
        host = default_config.get('host')
        print("No config found with Server section. Server settings default")

    return host

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():

    # Resource tree creation
    root = resource.Site()

    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['hello'], HelloResource())
    root.add_resource(['temp'], TempResource())
    # root.add_resource(['time'], TimeResource())
    # root.add_resource(['other', 'block'], BlockResource())
    # root.add_resource(['other', 'separate'], SeparateLargeResource())
    # root.add_resource(['whoami'], WhoAmI())

    host = read_config(config_ini="config.ini")

    await aiocoap.Context.create_server_context(root, bind=(host, None))

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
