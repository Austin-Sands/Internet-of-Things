#!/usr/bin/env python
import datetime
import logging
import configparser
from w1thermsensor import W1ThermSensor
from smbus import SMBus

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

    def get_temp(self):
        sensor = W1ThermSensor()
        currentTemp = sensor.get_temperature()
        message = "Current Temperature:" + str(format(currentTemp, '.1f')) + " C"
        self.content = bytes(message, 'utf-8')

    async def render_get(self, request):
        self.get_temp()
        return aiocoap.Message(payload=self.content)
    
class LightSensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.bus = SMBus(1)
        self.adc = 0x4b
        self.ldr = 0x84

    def get_light(self):
        self.bus.write_byte(self.adc, self.ldr)
        result = self.bus.read_byte(self.adc) / 255 * 3.3
        message = "Light Voltage: " + str(format(result, '.2f')) + " V"
        self.content = bytes(message, 'utf-8')
    
    async def render_get(self, request):
        self.get_light()
        return aiocoap.Message(payload=self.content)

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
    root.add_resource(['light'], LightSensorResource())

    host = read_config(config_ini="config.ini")

    await aiocoap.Context.create_server_context(root, bind=(host, None))

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
